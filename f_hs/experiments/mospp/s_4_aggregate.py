"""
===============================================================================
 Script: aggregate the `s_3` nested Results CSVs by k.

 Reads every raw per-(map, k) Results CSV produced by `s_3`
 from Drive `Results/`, collapses the 25-map sample down to
 ONE row per k (= the `m` start-count) by taking the MEAN of
 every metric column across maps, and writes the aggregates
 back to Drive `Results/agg/`.
-------------------------------------------------------------------------------
 Two outputs (the `Both` shape):

 (1) Per-config file  `Results/agg/{stem}_by_k.csv`
       One file per input config (mirrors the inputs). 20 rows
       (k = 10..200), columns = `m` + every metric column
       (`cnt_*`, `mem_*`, `elapsed_*`) meaned across the 25
       maps. The config (rule / depth) lives in the filename,
       exactly as in the raw inputs.

 (2) Combined table  `Results/agg/all_by_k.csv`
       Every config stacked into one long table, keyed by
       (`algo`, `rule_bpmx`, `depth_bpmx`, `depth_prop`, `m`) +
       the meaned metrics. One file to plot all configs / both
       algos (inc + rep) together.
-------------------------------------------------------------------------------
 What "aggregate by k" drops / keeps:
   - `m`                       -> GROUP KEY (one output row per value).
   - `cnt_* / pct_* / mem_*
      / elapsed_*`             -> MEAN across the 25 maps. The derived
                                  `pct_bpmx_lifts` is injected per ROW
                                  (via the report's `add_derived_columns`)
                                  BEFORE the mean, so the result is the
                                  "mean of per-map rates" the report
                                  documents -- not ratio-of-means.
   - `domain`, `map`           -> dropped (the axis we average over;
                                  a mean over map identities is
                                  meaningless).
   - `rule_bpmx`, `depth_bpmx`,
     `depth_prop`              -> constant within a file; encoded in
                                  the per-config FILENAME, and lifted
                                  to columns (+ an `algo` tag) only in
                                  the combined table so the stacked
                                  configs stay distinguishable.

 This makes `s_4` the single aggregation authority: its per-config
 `{stem}_by_k.csv` IS the `per_kc` frame `s_5` renders (one row per
 (config, k), every metric meaned, derived columns included), so
 `s_5` no longer downloads the raw per-map CSVs or re-aggregates.
-------------------------------------------------------------------------------
 f_psl/pandas usage: the aggregation IS `UDf.group(col_a='m',
 col_b=<metrics>, agg='mean')`; the stack IS `UDf.union`. Read
 / write via `UDf`. The only raw-pandas glue is lifting the
 constant config tags to columns + column reordering for the
 combined table (no `UDf` method covers a constant column).
-------------------------------------------------------------------------------
 Inputs  (Drive)  `Results/astar_inc_nested_*.csv`  (16 configs)
                  `Results/astar_rep_nested.csv`     (1 baseline)
                  `_toy*` smoke files are skipped.

 Outputs (Drive)  `Results/agg/{stem}_by_k.csv`  (one per input)
                  `Results/agg/all_by_k.csv`     (combined)

 Run (reads ~17 CSVs from Drive + uploads -- the user runs it):
   `python -m f_hs.experiments.mospp.s_4_aggregate`
===============================================================================
"""
import os
import tempfile
import logging

import pandas as pd

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_psl.pandas import UDf

from f_hs.experiments.mospp.report_render import (
    add_derived_columns, metric_columns,
)


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Drive locations ─────────────────────────────────────────────────────────

# Raw `s_3` Results live here; aggregates land in the `agg/`
# subfolder so they never shadow the raw inputs.
_DIR_IN = 'Results'
_DIR_OUT = 'Results/agg'

# Group key (the start-count k) + the config tag columns lifted
# into the combined table. Order = combined-table left columns.
_KEY = 'm'
_TAG_COLS = ('algo', 'rule_bpmx', 'depth_bpmx', 'depth_prop')


# ── File discovery ──────────────────────────────────────────────────────────

# Recognised raw-CSV prefixes -> algo tag, in priority order
# (more specific before the `astar_` inc fallback). The `s_3`
# runners write one of these.
_ALGO_PREFIXES: tuple[tuple[str, str], ...] = (
    ('astar_rep', 'rep'),
    ('astar_flip', 'flip'),
    ('bfs_flip', 'bfs'),
    ('dijkstra_flip', 'dijkstra'),
    ('astar_', 'inc'),        # fallback: the inc sweep configs
)


def _is_results_csv(name: str) -> bool:
    """
    ========================================================================
     True for a raw `s_3` nested Results CSV (inc / rep / flip /
     bfs / dijkstra), skipping `_toy*` smoke runs and any non-CSV /
     agg output.
    ========================================================================
    """
    return (name.endswith('.csv')
            and 'nested' in name
            and '_toy' not in name
            and any(name.startswith(p) for p, _ in _ALGO_PREFIXES))


def _algo_of(name: str) -> str:
    """
    ========================================================================
     Algorithm tag from the filename. Cross-variant families are
     matched by prefix: `astar_rep_*` -> 'rep', `astar_flip_*` ->
     'flip', `bfs_flip_*` -> 'bfs', `dijkstra_flip_*` -> 'dijkstra'.

     The `astar_inc_*` family shares ONE prefix but encodes its
     reuse-store config in filename TOKENS -- no DATA column carries
     `adaptive_h` / `carry_cache`, so without refinement the combined
     `all_by_k.csv` would collapse cache-only, cache+adapt, and
     adapt-no-cache onto a single 'inc' tag with the SAME
     (rule_bpmx, depth_bpmx, depth_prop) identity. So the inc family
     is split by tokens (the per-stem `_by_k.csv` files are already
     distinct by filename -- this only disambiguates the long table):

       `_adapt_1` + `_cacheoff` -> 'inc_adapt_nocache'  (ADAPT on, CACHE
                                    off -- pure Koenig 2005 Adaptive A*)
       `_adapt_1`               -> 'inc_adapt'  (cache + adaptive bound)
       `_cacheoff`              -> 'inc_nocache' (cache off, no adaptive
                                    -- equivalent to `rep`; edge case)
       (neither)                -> 'inc'  (cache-only -- the default sweep)
    ========================================================================
    """
    # Specific cross-variant families first; the inc family (the generic
    # `astar_` fallback prefix) is refined by tokens below.
    for prefix, tag in _ALGO_PREFIXES:
        if prefix == 'astar_':
            continue
        if name.startswith(prefix):
            return tag
    adapt = '_adapt_1' in name
    cacheoff = '_cacheoff' in name
    if adapt and cacheoff:
        return 'inc_adapt_nocache'
    if adapt:
        return 'inc_adapt'
    if cacheoff:
        return 'inc_nocache'
    return 'inc'


# ── Aggregation (pure -- no Drive) ──────────────────────────────────────────

def _aggregate_by_k(df: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     Collapse a raw per-(map, k) DataFrame to one row per k:
     group by `m`, MEAN every metric column across the 25 maps.
     Result columns = `m` + the metrics (`cnt_* / pct_* / mem_* /
     elapsed_*`, CSV order). This is the per-config output; the
     config stays in the filename.

     `add_derived_columns` is applied FIRST so the derived
     `pct_bpmx_lifts` (= `cnt_bpmx_lifts / cnt_bpmx_attempts`)
     is the per-(map, k) ROW rate; the subsequent mean is then
     the "mean of per-map rates" the report documents (NOT
     `mean(lifts) / mean(attempts)`, a size-weighted different
     quantity). This makes `s_4` the single aggregation authority
     whose output `s_5` renders directly. `metric_columns` (the
     report's selector, `cnt_/pct_/mem_/elapsed_`) picks the
     columns to mean; keys (`m`), ids (`domain`, `map`) and config
     tags are excluded.
    ========================================================================
    """
    df = add_derived_columns(df)
    return UDf.group(df=df, col_a=_KEY, col_b=metric_columns(df),
                     agg='mean')


def _tagged(agg: pd.DataFrame,
            src: pd.DataFrame,
            algo: str) -> pd.DataFrame:
    """
    ========================================================================
     Lift the constant config of `src` (the raw df) onto the
     per-k aggregate `agg`, for the combined table: prepend
     `algo` + the `rule_bpmx` / `depth_bpmx` / `depth_prop`
     values (constant within a config file -> read row 0), then
     order columns as TAGS + `m` + metrics so every config
     stacks union-compatibly.
    ========================================================================
    """
    out = agg.copy()
    out['algo'] = algo
    for c in ('rule_bpmx', 'depth_bpmx', 'depth_prop'):
        out[c] = src[c].iloc[0]
    metrics = [c for c in agg.columns if c != _KEY]
    return out[[*_TAG_COLS, _KEY, *metrics]]


# ── Orchestration (Drive I/O) ───────────────────────────────────────────────

def aggregate(dir_in: str = _DIR_IN,
              dir_out: str = _DIR_OUT) -> None:
    """
    ========================================================================
     Read every raw nested Results CSV from Drive `dir_in`,
     write a per-config `{stem}_by_k.csv` aggregate for each,
     and a single combined `all_by_k.csv`, all to Drive
     `dir_out`. Intermediates live in `/tmp` (Drive-only
     workflow); nothing is saved into the project tree.
    ========================================================================
    """
    drive = Drive.Factory.valdas()
    names = sorted(n for n in drive.files(path=dir_in)
                   if _is_results_csv(n))
    if not names:
        _log.warning(f'no raw Results CSVs under {dir_in!r} -- '
                     f'nothing to aggregate')
        return
    _log.info(f'aggregating {len(names)} config CSV(s) by k')

    parts: list[pd.DataFrame] = []
    for name in names:
        stem = os.path.splitext(name)[0]
        fd_in, path_in = tempfile.mkstemp(suffix='.csv')
        os.close(fd_in)
        fd_out, path_out = tempfile.mkstemp(suffix='.csv')
        os.close(fd_out)
        try:
            drive.download(path_src=f'{dir_in}/{name}',
                           path_dest=path_in)
            df = UDf.read(path=path_in)
            agg = _aggregate_by_k(df)
            UDf.write(df=agg, path=path_out)
            dest = f'{dir_out}/{stem}_by_k.csv'
            drive.upload(path_src=path_out, path_dest=dest)
            _log.info(f'  {name}: {len(df)} rows -> '
                      f'{len(agg)} by-k rows  ->  {dest}')
            parts.append(_tagged(agg, df, _algo_of(name)))
        finally:
            for p in (path_in, path_out):
                if os.path.exists(p):
                    os.unlink(p)

    # Combined long table -- stack every config (UNION ALL).
    combined = parts[0]
    for p in parts[1:]:
        combined = UDf.union(df_1=combined, df_2=p)
    fd_c, path_c = tempfile.mkstemp(suffix='.csv')
    os.close(fd_c)
    try:
        UDf.write(df=combined, path=path_c)
        dest = f'{dir_out}/all_by_k.csv'
        drive.upload(path_src=path_c, path_dest=dest)
        _log.info(f'combined: {len(combined)} rows '
                  f'({len(parts)} configs)  ->  {dest}')
    finally:
        if os.path.exists(path_c):
            os.unlink(path_c)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    aggregate()
    _log.info('--- done ---')
