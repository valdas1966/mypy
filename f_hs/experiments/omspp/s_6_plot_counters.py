"""
===============================================================================
 Script: plot kA*-INC (extended mode) vs kA*-AGG (8 configs, Φ=MIN)
 counters as a multi-page PDF on Drive.

 For each counter, one chart with:
   - 1 bold black line for kA*-INC (extended)
   - 8 lines for kA*-AGG, one per (is_lazy, is_opt, store_vector)
     configuration. Visual encoding:
       linestyle = is_lazy   (solid = lazy, dashed = eager)
       color     = (is_opt, store_vector) pair (4 colors)

 X-axis: k (number of goals).
 Y-axis: counter value, MEAN over (domain, map) at each k.

 Each page: chart on the top half, a per-k DATA TABLE on the bottom
 half (rows = k values, columns = INC + 8 AGG configs). The table
 surfaces the exact mean values that the chart visualizes -- useful
 when one line is visually crushed by another (e.g., INC's
 `cnt_h_search` is ~10^5 while some AGG configs reach ~10^7, so the
 INC line looks near-zero on a shared Y axis without log scaling).

 The two CSVs are inner-joined on `(domain, map, k)` first, so any
 (map, k) missing from one side (e.g. a partial 3rd chain in toy
 mode) is dropped from both -- the comparison stays apples-to-apples.

 Caveat on `mem_open` / `mem_closed` (AGG)
   The base `_sync_memory_snapshot` only counts the frontier struct +
   pro-rated g/parent slots. KAStarAgg's auxiliary structures --
   `_F_stored` (always), `_h_vector` (when store_vector=True),
   `_responsible` (when is_opt=True) -- are NOT included. AGG configs
   with sv / opt thus appear memory-cheaper than they really are; a
   footer note on the mem_* charts flags this.
-------------------------------------------------------------------------------
 14 charts total:
   12 shared counters  (INC + 8 AGG lines per chart)
     cnt_h_search, cnt_h_update,
     cnt_push, cnt_pop, cnt_decrease,
     cnt_expanded, cnt_generated,
     mem_open, mem_closed,
     elapsed_total, elapsed_search, elapsed_update
   2 AGG-only counters (8 AGG lines per chart, no INC)
     cnt_phi_search, cnt_phi_update
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/kastar_inc_extended{suffix}.csv
   Experiments/OMSPP/kastar_agg_all_configs{suffix}.csv

 Output  (Drive)
   Experiments/OMSPP/kastar_inc_vs_agg_counters{suffix}.pdf

 `suffix` is `''` for full-run CSVs or `'_toy{N}'` for toy CSVs.
===============================================================================
"""
import os
import tempfile
import logging

import pandas as pd
import matplotlib
matplotlib.use('Agg')   # headless: write PDF without a display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Counters shared between INC and AGG.
_SHARED_COUNTERS: list[str] = [
    'cnt_h_search',
    'cnt_h_update',
    'cnt_push',
    'cnt_pop',
    'cnt_decrease',
    'cnt_expanded',
    'cnt_generated',
    'mem_open',
    'mem_closed',
    'elapsed_total',
    'elapsed_search',
    'elapsed_update',
]

# Counters only in AGG (Φ-related).
_AGG_ONLY_COUNTERS: list[str] = [
    'cnt_phi_search',
    'cnt_phi_update',
]

# 8 AGG configs in canonical order.
_AGG_CONFIGS: list[tuple[bool, bool, bool, str]] = [
    (False, False, False, 'eager_noopt_nosv'),
    (False, False, True,  'eager_noopt_sv'),
    (False, True,  False, 'eager_opt_nosv'),
    (False, True,  True,  'eager_opt_sv'),
    (True,  False, False, 'lazy_noopt_nosv'),
    (True,  False, True,  'lazy_noopt_sv'),
    (True,  True,  False, 'lazy_opt_nosv'),
    (True,  True,  True,  'lazy_opt_sv'),
]

# Color per (is_opt, store_vector) pair.
_AGG_COLOR: dict[tuple[bool, bool], str] = {
    (False, False): 'tab:blue',
    (False, True):  'tab:orange',
    (True,  False): 'tab:green',
    (True,  True):  'tab:red',
}

# Linestyle per is_lazy.
_AGG_LINESTYLE: dict[bool, str] = {
    False: '--',   # eager
    True:  '-',    # lazy
}

_INC_COLOR = 'black'
_INC_LW = 2.6


# ── Drive I/O ──────────────────────────────────────────────────────────────

def _download_csv(drive: Drive, path: str) -> pd.DataFrame:
    """
    ========================================================================
     Download a CSV from Drive into a temp file and return it as a
     DataFrame. The temp file is cleaned up before returning.
    ========================================================================
    """
    fd, local = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    try:
        drive.download(path_src=path, path_dest=local)
        df = pd.read_csv(local)
        _log.info(f'loaded {path}: {len(df):,} rows, '
                  f'{len(df.columns)} cols')
        return df
    finally:
        if os.path.exists(local):
            os.unlink(local)


# ── Inner-join + per-k mean ─────────────────────────────────────────────────

def _intersect_keys(df_inc: pd.DataFrame,
                    df_agg: pd.DataFrame
                    ) -> pd.DataFrame:
    """
    ========================================================================
     Return the set of (domain, map, k) keys present in BOTH CSVs.
     Drives the inner-join filter applied to each frame before
     aggregation.
    ========================================================================
    """
    keys_inc = df_inc[['domain', 'map', 'k']].drop_duplicates()
    keys_agg = df_agg[['domain', 'map', 'k']].drop_duplicates()
    common = keys_inc.merge(keys_agg, on=['domain', 'map', 'k'])
    _log.info(f'common (domain, map, k) triples: {len(common):,}')
    return common


def _filter_common(df: pd.DataFrame,
                   common: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     Keep only rows of `df` whose (domain, map, k) appears in
     `common`. Returns the filtered DataFrame.
    ========================================================================
    """
    return df.merge(common, on=['domain', 'map', 'k'], how='inner')


# ── Plotting ────────────────────────────────────────────────────────────────

def _plot_counter(ax,
                  counter: str,
                  inc_by_k: pd.DataFrame | None,
                  agg_by_k_config: pd.DataFrame,
                  n_maps: int) -> None:
    """
    ========================================================================
     Draw one counter onto `ax`. `inc_by_k` may be None for
     AGG-only counters (cnt_phi_*).
    ========================================================================
    """
    if inc_by_k is not None and counter in inc_by_k.columns:
        ax.plot(inc_by_k.index, inc_by_k[counter],
                color=_INC_COLOR, linewidth=_INC_LW,
                marker='o', markersize=4,
                label='KAStarInc (extended)')

    for is_lazy, is_opt, store_vector, cfg in _AGG_CONFIGS:
        try:
            series = agg_by_k_config.xs(cfg, level='config')[counter]
        except KeyError:
            continue
        ax.plot(series.index, series.values,
                color=_AGG_COLOR[(is_opt, store_vector)],
                linestyle=_AGG_LINESTYLE[is_lazy],
                linewidth=1.4,
                label=f'KAStarAgg/{cfg}')

    ax.set_xlabel('k (number of goals)')
    ax.set_ylabel(counter)
    ax.set_title(f'{counter}  '
                 f'(mean over {n_maps} (domain, map) at each k)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=7, framealpha=0.85)

    # Caveat note for memory snapshots -- AGG's _F_stored,
    # _h_vector, _responsible are NOT counted by mem_open /
    # mem_closed.
    if counter in ('mem_open', 'mem_closed'):
        ax.text(0.01, -0.16,
                'Caveat: AGG\'s _F_stored / _h_vector (sv) / '
                '_responsible (opt) are NOT in mem_* '
                '(see _sync_memory_snapshot).',
                transform=ax.transAxes,
                fontsize=7, color='dimgray', style='italic')


def _format_value(counter: str, value: float) -> str:
    """
    ========================================================================
     Format a single mean value for the per-k data table. Elapsed
     counters get 3 decimals; large counts use scientific notation;
     smaller integer-valued counters use thousands-separator.
    ========================================================================
    """
    if pd.isna(value):
        return '—'
    if counter.startswith('elapsed_'):
        return f'{value:.3f}'
    if abs(value) >= 1_000_000:
        return f'{value:.2e}'
    return f'{value:,.0f}'


def _render_table(ax,
                  counter: str,
                  inc_by_k: pd.DataFrame | None,
                  agg_by_k_config: pd.DataFrame) -> None:
    """
    ========================================================================
     Render the per-k data table on `ax`. Columns: 'k' + 'INC' (if
     applicable) + 8 AGG configs. Rows: 20 k values.
    ========================================================================
    """
    ax.axis('off')
    ks = sorted(agg_by_k_config.index.get_level_values('k').unique())

    has_inc = (inc_by_k is not None
               and counter in inc_by_k.columns)
    col_labels: list[str] = ['k']
    if has_inc:
        col_labels.append('INC')
    for _, _, _, cfg in _AGG_CONFIGS:
        col_labels.append(cfg)

    cells: list[list[str]] = []
    for k in ks:
        row: list[str] = [str(k)]
        if has_inc:
            row.append(_format_value(counter, inc_by_k.loc[k, counter]))
        for _, _, _, cfg in _AGG_CONFIGS:
            try:
                val = agg_by_k_config.xs(
                    cfg, level='config').loc[k, counter]
            except KeyError:
                val = float('nan')
            row.append(_format_value(counter, val))
        cells.append(row)

    table = ax.table(cellText=cells,
                     colLabels=col_labels,
                     cellLoc='right',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(6.5)
    table.scale(1.0, 1.18)
    # Bold header row.
    for j in range(len(col_labels)):
        table[(0, j)].set_text_props(weight='bold')
    # Bold the 'k' column.
    for i in range(1, len(cells) + 1):
        table[(i, 0)].set_text_props(weight='bold')


# ── Public API ─────────────────────────────────────────────────────────────

def make_plots(path_drive_csv_inc: str,
               path_drive_csv_agg: str,
               path_drive_pdf_out: str) -> None:
    """
    ============================================================================
     Read the INC and AGG CSVs from Drive, inner-join on
     (domain, map, k), aggregate each counter to a per-k mean,
     and write a 14-page PDF (one chart per counter) to Drive.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    df_inc = _download_csv(drive=drive, path=path_drive_csv_inc)
    df_agg = _download_csv(drive=drive, path=path_drive_csv_agg)

    # Inner-join keys so the comparison is apples-to-apples.
    common = _intersect_keys(df_inc=df_inc, df_agg=df_agg)
    df_inc = _filter_common(df=df_inc, common=common)
    df_agg = _filter_common(df=df_agg, common=common)
    n_maps = common.drop_duplicates(['domain', 'map']).shape[0]
    _log.info(f'after filter: INC={len(df_inc):,} rows, '
              f'AGG={len(df_agg):,} rows; n_maps={n_maps}')

    # Per-k aggregations.
    inc_cols = [c for c in _SHARED_COUNTERS if c in df_inc.columns]
    inc_by_k = df_inc.groupby('k')[inc_cols].mean()
    agg_cols = _SHARED_COUNTERS + _AGG_ONLY_COUNTERS
    agg_cols = [c for c in agg_cols if c in df_agg.columns]
    agg_by_k_config = df_agg.groupby(['k', 'config'])[agg_cols].mean()

    # Write multi-page PDF.
    fd, path_pdf = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    try:
        with PdfPages(path_pdf) as pdf:
            # Shared counters: INC + 8 AGG lines + per-k table.
            for counter in _SHARED_COUNTERS:
                fig = plt.figure(figsize=(13, 9.5))
                gs = fig.add_gridspec(2, 1,
                                      height_ratios=[3, 2],
                                      hspace=0.35)
                ax_chart = fig.add_subplot(gs[0])
                ax_table = fig.add_subplot(gs[1])
                _plot_counter(ax=ax_chart,
                              counter=counter,
                              inc_by_k=inc_by_k,
                              agg_by_k_config=agg_by_k_config,
                              n_maps=n_maps)
                _render_table(ax=ax_table,
                              counter=counter,
                              inc_by_k=inc_by_k,
                              agg_by_k_config=agg_by_k_config)
                pdf.savefig(fig)
                plt.close(fig)

            # AGG-only counters: 8 AGG lines + per-k table (no INC).
            for counter in _AGG_ONLY_COUNTERS:
                fig = plt.figure(figsize=(13, 9.5))
                gs = fig.add_gridspec(2, 1,
                                      height_ratios=[3, 2],
                                      hspace=0.35)
                ax_chart = fig.add_subplot(gs[0])
                ax_table = fig.add_subplot(gs[1])
                _plot_counter(ax=ax_chart,
                              counter=counter,
                              inc_by_k=None,
                              agg_by_k_config=agg_by_k_config,
                              n_maps=n_maps)
                _render_table(ax=ax_table,
                              counter=counter,
                              inc_by_k=None,
                              agg_by_k_config=agg_by_k_config)
                pdf.savefig(fig)
                plt.close(fig)
        _log.info(f'wrote {path_pdf}')
        drive.upload(path_src=path_pdf,
                     path_dest=path_drive_pdf_out)
        _log.info(f'uploaded -> {path_drive_pdf_out}')
    finally:
        if os.path.exists(path_pdf):
            os.unlink(path_pdf)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Default: pick up the toy outputs already on Drive. Set
    # suffix = '' to point at full-run CSVs once they exist.
    suffix = '_toy50'
    path_drive_csv_inc = (f'Experiments/OMSPP/'
                          f'kastar_inc_extended{suffix}.csv')
    path_drive_csv_agg = (f'Experiments/OMSPP/'
                          f'kastar_agg_all_configs{suffix}.csv')
    path_drive_pdf_out = (f'Experiments/OMSPP/'
                          f'kastar_inc_vs_agg_counters{suffix}.pdf')

    make_plots(path_drive_csv_inc=path_drive_csv_inc,
               path_drive_csv_agg=path_drive_csv_agg,
               path_drive_pdf_out=path_drive_pdf_out)
    _log.info('--- done ---')
