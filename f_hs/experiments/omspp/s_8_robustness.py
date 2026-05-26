"""
===============================================================================
 Script: cluster-bootstrap robustness analysis for the OMSPP INC vs AGG
 comparison.

 For each available BATCH ('orig', 'extra', 'combined') and each
 (k, metric) pair, compute a 95% confidence interval on the AGG / INC
 ratio using a CLUSTER bootstrap over (domain, map) tuples.

 Why cluster bootstrap
   Chains within the same (domain, map) share grid topology (start
   cells / goal cluster geometry vary, the underlying graph does
   not), so they are NOT exchangeable across maps. Cluster bootstrap
   resamples maps with replacement -- the correct unit of independent
   variation. Bumping `n_per_map` in s_3 reduces within-cluster noise
   but cannot shrink between-cluster variance, so the CI width is
   bounded by between-map variability.

 Decision gate
   A (batch, k, metric) is declared ROBUST iff the CI half-width is at
   most `_GATE_FRAC` (default 10%) of the effect magnitude
   |mean_ratio - 1|. The script prints a per-batch / per-metric
   pass-rate over the k-buckets and uploads the per-row results.

 Output (Drive)
   Experiments/OMSPP/robustness.csv
   Columns: batch, n_clusters, n_per_cluster, k, metric,
            mean_ratio, ci_lo, ci_hi, half_width,
            target_half_width, robust
-------------------------------------------------------------------------------
 Headline metrics
   MEM_TOTAL  = mem_open + mem_closed
   MEM_OPEN   = mem_open       (AGG aux peak is folded in here)
   MEM_CLOSED = mem_closed
   CNT_H_TOTAL = cnt_h_search + cnt_h_update + cnt_decrease  (INC)
                 cnt_h_search + cnt_h_update                  (AGG)
   CNT_EXPANDED = cnt_expanded

 AGG rows are filtered to `_AGG_CONFIG = 'lazy_opt_sv'` -- the
 canonical INC-vs-AGG comparison config (see 2026-05-23 session).

 No KAStarInc / KAStarAgg runs here -- pure CSV post-processing.
===============================================================================
"""
import csv
import io
import logging
import os
import random
import statistics
import tempfile
from collections import defaultdict

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Drive paths ────────────────────────────────────────────────────────────

_PATH_INC_ORIG  = 'Experiments/OMSPP/kastar_inc_extended.csv'
_PATH_INC_EXTRA = 'Experiments/OMSPP/kastar_inc_extended_extra.csv'
_PATH_AGG_ORIG  = 'Experiments/OMSPP/kastar_agg_all_configs.csv'
_PATH_AGG_EXTRA = 'Experiments/OMSPP/kastar_agg_all_configs_extra.csv'
_PATH_OUT       = 'Experiments/OMSPP/robustness.csv'


# ── Analysis config ────────────────────────────────────────────────────────

# Headline AGG config for the INC-vs-AGG comparison.
_AGG_CONFIG = 'lazy_opt_sv'

# Cluster bootstrap parameters.
_BOOTSTRAP_B = 5_000
_BOOTSTRAP_SEED = 42
_CI_ALPHA = 0.05    # 95% CI

# Decision rule: half_width <= _GATE_FRAC * |mean_ratio - 1|.
_GATE_FRAC = 0.10

# Metric registry (display name -> readers).
_METRICS = [
    'MEM_TOTAL',
    'MEM_OPEN',
    'MEM_CLOSED',
    'CNT_H_TOTAL',
    'CNT_EXPANDED',
]

# Output CSV columns.
_OUT_COLS = [
    'batch',
    'n_clusters',
    'n_per_cluster',
    'k',
    'metric',
    'mean_ratio',
    'ci_lo',
    'ci_hi',
    'half_width',
    'target_half_width',
    'robust',
]


# ── Metric readers ─────────────────────────────────────────────────────────

def _inc_metric_value(row: dict, metric: str) -> float:
    """
    ========================================================================
     Extract one numeric value of `metric` from one INC CSV row.
    ========================================================================
    """
    if metric == 'CNT_H_TOTAL':
        return (float(row['cnt_h_search'])
                + float(row['cnt_h_update'])
                + float(row['cnt_decrease']))
    if metric == 'CNT_EXPANDED':
        return float(row['cnt_expanded'])
    if metric == 'MEM_OPEN':
        return float(row['mem_open'])
    if metric == 'MEM_CLOSED':
        return float(row['mem_closed'])
    if metric == 'MEM_TOTAL':
        return float(row['mem_open']) + float(row['mem_closed'])
    raise ValueError(f'unknown metric: {metric}')


def _agg_metric_value(row: dict, metric: str) -> float:
    """
    ========================================================================
     Extract one numeric value of `metric` from one AGG CSV row.

     `cnt_h_total` for AGG omits `cnt_decrease` (decrease-key h-calls
     are an INC-specific bookkeeping cost; AGG doesn't share that
     accounting).
    ========================================================================
    """
    if metric == 'CNT_H_TOTAL':
        return (float(row['cnt_h_search'])
                + float(row['cnt_h_update']))
    if metric == 'CNT_EXPANDED':
        return float(row['cnt_expanded'])
    if metric == 'MEM_OPEN':
        return float(row['mem_open'])
    if metric == 'MEM_CLOSED':
        return float(row['mem_closed'])
    if metric == 'MEM_TOTAL':
        return float(row['mem_open']) + float(row['mem_closed'])
    raise ValueError(f'unknown metric: {metric}')


# ── Drive helpers ──────────────────────────────────────────────────────────

def _read_csv(drive: Drive, path: str) -> list[dict] | None:
    """
    ========================================================================
     Read one CSV from Drive as a list of dicts. Returns None when the
     file is absent (caller decides whether that is a hard error).
    ========================================================================
    """
    if not drive.is_exists(path=path):
        _log.warning(f'  {path}: NOT FOUND on Drive')
        return None
    text = drive.read(path=path).text
    rows = list(csv.DictReader(io.StringIO(text)))
    _log.info(f'  {path}: {len(rows):,} rows')
    return rows


# ── Aggregation ────────────────────────────────────────────────────────────

def _per_cluster_ratios(rows_inc: list[dict],
                        rows_agg: list[dict],
                        k: int,
                        metric: str,
                        ) -> dict[tuple[str, str], float]:
    """
    ============================================================================
     For one (k, metric), build a dict mapping each cluster
     `(domain, map)` to its mean ratio AGG / INC.

     Within a cluster we average INC and AGG values across all chains
     present (one chain when n_per_map=1, more in the extras batch),
     then divide cluster-mean(AGG) / cluster-mean(INC).

     AGG rows are filtered to `_AGG_CONFIG` (canonical comparison).
    ============================================================================
    """
    inc_by: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows_inc:
        if int(r['k']) != k:
            continue
        inc_by[(r['domain'], r['map'])].append(
            _inc_metric_value(row=r, metric=metric))

    agg_by: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows_agg:
        if int(r['k']) != k:
            continue
        if r.get('config') != _AGG_CONFIG:
            continue
        agg_by[(r['domain'], r['map'])].append(
            _agg_metric_value(row=r, metric=metric))

    ratios: dict[tuple[str, str], float] = {}
    for key, inc_vals in inc_by.items():
        agg_vals = agg_by.get(key, [])
        if not agg_vals or not inc_vals:
            continue
        mean_inc = statistics.fmean(inc_vals)
        if mean_inc == 0.0:
            continue
        mean_agg = statistics.fmean(agg_vals)
        ratios[key] = mean_agg / mean_inc
    return ratios


def _cluster_bootstrap_ci(values: list[float],
                          B: int = _BOOTSTRAP_B,
                          alpha: float = _CI_ALPHA,
                          seed: int = _BOOTSTRAP_SEED,
                          ) -> tuple[float, float, float]:
    """
    ============================================================================
     Percentile cluster bootstrap on the mean of `values` (one entry
     per cluster). Returns `(mean, ci_lo, ci_hi)`.
    ============================================================================
    """
    n = len(values)
    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(B):
        s = 0.0
        for _ in range(n):
            s += values[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[int((alpha / 2.0) * B)]
    hi = means[int((1.0 - alpha / 2.0) * B) - 1]
    return statistics.fmean(values), lo, hi


def _chains_per_cluster(rows_inc: list[dict], k0: int) -> float:
    """
    ========================================================================
     Mean INC chains per cluster, sampled at k=k0. Sanity number for
     the output CSV (1.0 for the canonical orig batch).
    ========================================================================
    """
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for r in rows_inc:
        if int(r['k']) == k0:
            counts[(r['domain'], r['map'])] += 1
    if not counts:
        return 0.0
    return statistics.fmean(counts.values())


# ── Public API ─────────────────────────────────────────────────────────────

def analyse_robustness(path_drive_inc_orig: str = _PATH_INC_ORIG,
                       path_drive_inc_extra: str = _PATH_INC_EXTRA,
                       path_drive_agg_orig: str = _PATH_AGG_ORIG,
                       path_drive_agg_extra: str = _PATH_AGG_EXTRA,
                       path_drive_csv_out: str = _PATH_OUT,
                       ) -> None:
    """
    ============================================================================
     Read INC + AGG benchmark CSVs from Drive (canonical + optional
     `_extra` batch), and for each available batch
     ('orig' / 'extra' / 'combined') compute per-k cluster-bootstrap
     CIs on AGG/INC for the headline metrics.

     'extra' / 'combined' are skipped silently when the `_extra` CSVs
     are absent on Drive (e.g., the user has not yet run s_3/s_4/s_5
     with `IS_EXTRA=True`).

     Uploads `robustness.csv` to Drive and prints a per-batch pass-rate.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info('reading benchmark CSVs from Drive:')
    inc_orig = _read_csv(drive=drive, path=path_drive_inc_orig)
    inc_extra = _read_csv(drive=drive, path=path_drive_inc_extra)
    agg_orig = _read_csv(drive=drive, path=path_drive_agg_orig)
    agg_extra = _read_csv(drive=drive, path=path_drive_agg_extra)

    if not inc_orig or not agg_orig:
        raise FileNotFoundError(
            f'orig INC + AGG CSVs are required; '
            f'inc_orig={bool(inc_orig)}, agg_orig={bool(agg_orig)}')

    # Build the batches we can analyse.
    batches: list[tuple[str, list[dict], list[dict]]] = [
        ('orig', inc_orig, agg_orig),
    ]
    if inc_extra and agg_extra:
        batches.append(('extra', inc_extra, agg_extra))
        batches.append(('combined',
                        inc_orig + inc_extra,
                        agg_orig + agg_extra))
    else:
        _log.warning('extras CSVs not found -- analysing orig only. '
                     'Run s_3/s_4/s_5 with IS_EXTRA=True to enable '
                     'the `extra` and `combined` batches.')

    # k-grid from the orig INC CSV (all batches share the same k grid).
    ks = sorted({int(r['k']) for r in inc_orig})
    k0 = ks[0]

    out_rows: list[dict] = []
    for batch_name, inc_rows, agg_rows in batches:
        _log.info(f'--- batch: {batch_name} ---')
        n_per_cluster = _chains_per_cluster(rows_inc=inc_rows, k0=k0)
        for metric in _METRICS:
            n_pass = 0
            n_total = 0
            for k in ks:
                ratios = _per_cluster_ratios(rows_inc=inc_rows,
                                             rows_agg=agg_rows,
                                             k=k,
                                             metric=metric)
                values = list(ratios.values())
                if len(values) < 2:
                    continue
                mean, lo, hi = _cluster_bootstrap_ci(values=values)
                half_width = (hi - lo) / 2.0
                target = _GATE_FRAC * abs(mean - 1.0)
                robust = (target > 0.0) and (half_width <= target)
                out_rows.append({
                    'batch':              batch_name,
                    'n_clusters':         len(values),
                    'n_per_cluster':      round(n_per_cluster, 2),
                    'k':                  k,
                    'metric':             metric,
                    'mean_ratio':         round(mean, 4),
                    'ci_lo':              round(lo, 4),
                    'ci_hi':              round(hi, 4),
                    'half_width':         round(half_width, 4),
                    'target_half_width':  round(target, 4),
                    'robust':             robust,
                })
                n_total += 1
                n_pass += int(robust)
            _log.info(f'  {metric}: '
                      f'{n_pass}/{n_total} k-buckets pass the '
                      f'{int(_GATE_FRAC * 100)}%-of-effect gate')

    # Write + upload.
    fd, path_local = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    try:
        with open(path_local, 'w', newline='') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=_OUT_COLS,
                                    extrasaction='ignore')
            writer.writeheader()
            for row in out_rows:
                writer.writerow(row)
        drive.upload(path_src=path_local,
                     path_dest=path_drive_csv_out)
        _log.info(f'uploaded csv -> {path_drive_csv_out} '
                  f'({len(out_rows):,} rows)')
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    analyse_robustness()
    _log.info('--- done ---')
