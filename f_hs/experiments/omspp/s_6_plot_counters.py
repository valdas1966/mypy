"""
===============================================================================
 Script: plot kA*-INC (extended mode) vs kA*-AGG (2 configs, Φ=MIN)
 counters as a multi-page PDF on Drive.

 For each counter, one chart with:
   - 1 bold black line for kA*-INC (extended)
   - 2 lines for kA*-AGG: `eager_opt_sv` and `lazy_opt_sv`
     (restricted sweep, 2026-05-15). Visual encoding:
       linestyle = is_lazy   (solid = lazy, dashed = eager)
       color     = (is_opt, store_vector) pair (red for opt+sv)

 X-axis: k (number of goals).
 Y-axis: counter value, MEAN over (domain, map) at each k.

 Each page: chart on the top half, a per-k DATA TABLE on the bottom
 half (rows = k values, columns = INC + 2 AGG configs). The table
 surfaces the exact mean values that the chart visualizes -- useful
 when one line is visually crushed by another (e.g., INC's
 `cnt_h_search` is ~10^5 while some AGG configs reach ~10^7, so the
 INC line looks near-zero on a shared Y axis without log scaling).

 The two CSVs are inner-joined on `(domain, map, k)` first, so any
 (map, k) missing from one side (e.g. a partial 3rd chain in toy
 mode) is dropped from both -- the comparison stays apples-to-apples.

 Memory accounting
   `mem_open` / `mem_closed` cover frontier struct + pro-rated g/parent
   slots (strict bucket semantics). `mem_aux` covers KAStarAgg's
   auxiliary per-state structures that live OUTSIDE OPEN/CLOSED:
   `_F_stored` (always), `_h_vector` (when store_vector=True),
   `_responsible` (when is_opt=True). For KAStarInc this is
   structurally 0 -- no AGG-style aux structures exist. The
   derived headline `mem_total = mem_open + mem_closed + mem_aux`
   is added in `make_plots` (not stored in either CSV).
-------------------------------------------------------------------------------
 16 charts total:
   14 shared counters  (INC + 2 AGG lines per chart)
     cnt_h_search, cnt_h_update,
     cnt_push, cnt_pop, cnt_decrease,
     cnt_expanded, cnt_generated,
     mem_open, mem_closed, mem_aux, mem_total,
     elapsed_total, elapsed_search, elapsed_update
   2 AGG-only counters (2 AGG lines per chart, no INC)
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
    'mem_aux',
    'mem_total',
    'elapsed_total',
    'elapsed_search',
    'elapsed_update',
]

# Counters only in AGG (Φ-related).
_AGG_ONLY_COUNTERS: list[str] = [
    'cnt_phi_search',
    'cnt_phi_update',
]

# 2 AGG configs (matches s_5 restricted sweep, 2026-05-15).
# Restored to 8 if the no-opt / no-sv baselines are re-measured.
_AGG_CONFIGS: list[tuple[bool, bool, bool, str]] = [
    (False, True,  True,  'eager_opt_sv'),
    (True,  True,  True,  'lazy_opt_sv'),
]

# Three-algorithm color scheme: black (INC), blue (eager_opt_sv),
# red (lazy_opt_sv). Linestyle stays solid for all -- color alone
# distinguishes the three algorithms.
_AGG_COLOR: dict[bool, str] = {
    False: 'tab:blue',   # eager_opt_sv
    True:  'tab:red',    # lazy_opt_sv
}

_INC_COLOR = 'black'
_INC_LW = 2.6
_AGG_LW = 2.0


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
                color=_AGG_COLOR[is_lazy],
                linewidth=_AGG_LW,
                marker='o', markersize=4,
                label=f'KAStarAgg/{cfg}')

    ax.set_xlabel('k (number of goals)')
    ax.set_ylabel(counter)
    ax.set_title(f'{counter}  '
                 f'(mean over {n_maps} (domain, map) at each k)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=7, framealpha=0.85)

    # Memory accounting note: mem_open / mem_closed are strict
    # (frontier + pro-rated g/parent slots); AGG's auxiliary
    # structures live in mem_aux instead.
    if counter in ('mem_open', 'mem_closed'):
        ax.text(0.01, -0.16,
                'Strict bucket: frontier + g/parent slots only. '
                'AGG\'s _F_stored / _h_vector (sv) / '
                '_responsible (opt) are tallied in mem_aux.',
                transform=ax.transAxes,
                fontsize=7, color='dimgray', style='italic')
    elif counter == 'mem_aux':
        ax.text(0.01, -0.16,
                'AGG-only: _F_stored (always) + _h_vector (sv) + '
                '_responsible (opt). INC is structurally 0 -- no '
                'AGG-style aux structures.',
                transform=ax.transAxes,
                fontsize=7, color='dimgray', style='italic')
    elif counter == 'mem_total':
        ax.text(0.01, -0.16,
                'Headline memory metric: mem_open + mem_closed + '
                'mem_aux. For INC the aux term is 0 by construction;'
                ' for AGG it adds the _F_stored / vector / opt cost.',
                transform=ax.transAxes,
                fontsize=7, color='dimgray', style='italic')


def _format_value(counter: str, value: float) -> str:
    """
    ========================================================================
     Format a single mean value for the per-k data table. Elapsed
     counters get 3 decimals; large counts use K / M / B suffixes
     for readability (no scientific notation):
       >= 1e9  -> 1.23B
       >= 1e6  -> 1.23M
       >= 1e4  -> 12.3K   (use shorthand only past 10K so 1234 -> 1,234)
       else    -> thousands-separator
    ========================================================================
    """
    if pd.isna(value):
        return '—'
    if counter.startswith('elapsed_'):
        return f'{value:.3f}'
    av = abs(value)
    if av >= 1_000_000_000:
        return f'{value / 1_000_000_000:.2f}B'
    if av >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    if av >= 10_000:
        return f'{value / 1_000:.1f}K'
    return f'{value:,.0f}'


def _render_table(ax,
                  counter: str,
                  inc_by_k: pd.DataFrame | None,
                  agg_by_k_config: pd.DataFrame) -> None:
    """
    ========================================================================
     Render the per-k data table on `ax`. Columns: 'k' + 'INC' (if
     applicable) + 2 AGG configs. Rows: 20 k values.

     Cells are center-aligned and shaded with a per-row red-yellow-
     green gradient: the row's max is red, min is green, others are
     linearly interpolated. `k` and header cells are not shaded.
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

    # Build cells (display strings) AND raw values (for coloring) in
    # parallel. NaN entries in raw -> '—' string + no shading.
    cells: list[list[str]] = []
    raw: list[list[float]] = []
    for k in ks:
        row_str: list[str] = [str(k)]
        row_val: list[float] = [float('nan')]  # k column never shaded
        if has_inc:
            v = inc_by_k.loc[k, counter]
            row_str.append(_format_value(counter, v))
            row_val.append(float(v) if not pd.isna(v) else float('nan'))
        for _, _, _, cfg in _AGG_CONFIGS:
            try:
                v = agg_by_k_config.xs(
                    cfg, level='config').loc[k, counter]
            except KeyError:
                v = float('nan')
            row_str.append(_format_value(counter, v))
            row_val.append(float(v) if not pd.isna(v) else float('nan'))
        cells.append(row_str)
        raw.append(row_val)

    table = ax.table(cellText=cells,
                     colLabels=col_labels,
                     cellLoc='center',
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

    # Per-row red->yellow->green gradient on the data columns
    # (j >= 1). Max value in the row = red, min = green, others
    # linearly interpolated. Softened toward white for readable
    # text. Skip rows with < 2 finite values, or all-equal rows.
    cmap = plt.get_cmap('RdYlGn_r')
    softness = 0.55  # 0 = full saturation, 1 = pure white
    for i_row, vals in enumerate(raw, start=1):
        data_vals = [v for v in vals[1:] if not pd.isna(v)]
        if len(data_vals) < 2:
            continue
        vmin, vmax = min(data_vals), max(data_vals)
        if vmin == vmax:
            continue
        for j in range(1, len(vals)):
            v = vals[j]
            if pd.isna(v):
                continue
            pos = (v - vmin) / (vmax - vmin)
            r, g, b, _ = cmap(pos)
            r = 1 - (1 - r) * (1 - softness)
            g = 1 - (1 - g) * (1 - softness)
            b = 1 - (1 - b) * (1 - softness)
            table[(i_row, j)].set_facecolor((r, g, b))


# ── Public API ─────────────────────────────────────────────────────────────

def make_plots(path_drive_csv_inc: str,
               path_drive_csv_agg: str,
               path_drive_pdf_out: str) -> None:
    """
    ============================================================================
     Read the INC and AGG CSVs from Drive, derive `mem_total`
     (mem_open + mem_closed + mem_aux), inner-join on
     (domain, map, k), aggregate each counter to a per-k mean,
     and write a 16-page PDF (one chart per counter) to Drive.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    df_inc = _download_csv(drive=drive, path=path_drive_csv_inc)
    df_agg = _download_csv(drive=drive, path=path_drive_csv_agg)

    # Derived headline memory metric: total bytes carried by the
    # algorithm = strict OPEN bucket + strict CLOSED bucket + aux
    # structures (AGG-only; INC's mem_aux is structurally 0).
    df_inc['mem_total'] = (df_inc['mem_open']
                           + df_inc['mem_closed']
                           + df_inc['mem_aux'])
    df_agg['mem_total'] = (df_agg['mem_open']
                           + df_agg['mem_closed']
                           + df_agg['mem_aux'])

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
            # Shared counters: INC + 2 AGG lines + per-k table.
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

            # AGG-only counters: 2 AGG lines + per-k table (no INC).
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
    # Full-run CSVs (2026-05-15). Switch to '_toy50' to read the
    # historical 8-config toy snapshot.
    suffix = ''
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
