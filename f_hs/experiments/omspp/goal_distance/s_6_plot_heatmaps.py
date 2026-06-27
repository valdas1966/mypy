"""
===============================================================================
 goal_distance step s_6 -- plot the (min_dist x max_steps) phase diagram of
 the AGG / INC ratio as a multi-page PDF on Drive.

 One page per headline metric:
   expanded nodes (cnt_expanded), runtime (elapsed_total),
   memory (mem_total = mem_open + mem_closed).

 Each page shows, per AGG mode (eager_opt_sv / lazy_opt_sv):
   - a 5x5 heatmap of the mean AGG/INC ratio over (min_dist rows x
     max_steps cols); a ratio > 1 means INC wins (AGG costs more). Cells
     with no data (geometry-thinned / region < k) are greyed.
   - two marginal line plots collapsing each axis (ratio vs max_steps
     averaged over min_dist; ratio vs min_dist averaged over max_steps) --
     the two main effects, with eager and lazy overlaid.

 Ratios are PAIRED: computed per (domain, map, min_dist, max_steps)
 instance (AGG metric / INC metric), then averaged over maps per cell --
 the variance-cancelling unit for the within-map design.

 The INC and AGG CSVs are inner-joined on (domain, map, min_dist,
 max_steps) first, so any instance missing from one side is dropped from
 both -- the comparison stays apples-to-apples.
-------------------------------------------------------------------------------
 Memory accounting
   mem_total = mem_open + mem_closed for BOTH algos (AGG's aux peak is
   folded into mem_open by KAStarAgg, per the 2026-05-23 merge), so the
   cross-algo schema is just mem_open / mem_closed.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/goal_distance/kastar_inc_grid.csv
   Experiments/OMSPP/goal_distance/kastar_agg_grid.csv
 Output  (Drive)
   Experiments/OMSPP/goal_distance/inc_vs_agg_phase.pdf
===============================================================================
"""
import os
import tempfile
import logging

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # headless: write PDF without a display
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.backends.backend_pdf import PdfPages

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Phase-diagram axes (must match s_2 / s_3).
_MIN_DISTS = [100, 200, 300, 400, 500]   # heatmap rows (top -> bottom)
_MAX_STEPS = [20, 30, 40, 50, 60]        # heatmap cols (left -> right)

# Join keys identifying one phase-diagram instance.
_KEYS = ['domain', 'map', 'min_dist', 'max_steps']

# AGG modes compared against INC: (config label, display name, colour).
_AGG_MODES: list[tuple[str, str, str]] = [
    ('eager_opt_sv', 'AGG-Eager', 'tab:blue'),
    ('lazy_opt_sv',  'AGG-Lazy',  'tab:red'),
]

# Headline metrics: (column, display title).
_METRICS: list[tuple[str, str]] = [
    ('cnt_expanded', 'expanded nodes'),
    ('elapsed_total', 'runtime (s)'),
    ('mem_total', 'memory (mem_open + mem_closed)'),
]


# ── Drive I/O ──────────────────────────────────────────────────────────────

def _download_csv(drive: Drive, path: str) -> pd.DataFrame:
    """
    ============================================================================
     Download a CSV from Drive into a temp file and return it as a
     DataFrame; the temp file is cleaned up before returning.
    ============================================================================
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


# ── Ratio assembly ──────────────────────────────────────────────────────────

def _ratio_long(df_inc: pd.DataFrame,
                df_agg_cfg: pd.DataFrame,
                metric: str) -> pd.DataFrame:
    """
    ============================================================================
     Inner-join INC and one AGG config on `_KEYS` and return a frame with
     the per-instance paired ratio `ratio = agg[metric] / inc[metric]`
     (rows where INC metric == 0 are dropped to avoid div-by-zero).
    ============================================================================
    """
    left = df_inc[_KEYS + [metric]].rename(columns={metric: 'inc'})
    right = df_agg_cfg[_KEYS + [metric]].rename(columns={metric: 'agg'})
    merged = left.merge(right, on=_KEYS, how='inner')
    merged = merged[merged['inc'] != 0].copy()
    merged['ratio'] = merged['agg'] / merged['inc']
    return merged


def _ratio_matrix(ratios: pd.DataFrame) -> np.ndarray:
    """
    ============================================================================
     Pivot per-instance ratios to a 5x5 matrix of cell means, indexed by
     `_MIN_DISTS` (rows) x `_MAX_STEPS` (cols). Missing cells are NaN.
    ============================================================================
    """
    pivot = ratios.pivot_table(index='min_dist',
                               columns='max_steps',
                               values='ratio',
                               aggfunc='mean')
    pivot = pivot.reindex(index=_MIN_DISTS, columns=_MAX_STEPS)
    return pivot.to_numpy(dtype=float)


# ── Plotting ────────────────────────────────────────────────────────────────

def _draw_heatmap(ax,
                  matrix: np.ndarray,
                  title: str) -> None:
    """
    ============================================================================
     Draw one AGG/INC ratio heatmap. Diverging colour map centred at
     1.0 (green = ratio > 1 = INC wins; red = ratio < 1 = AGG wins). NaN
     cells (no data) are greyed. Each cell is annotated with its ratio.
    ============================================================================
    """
    masked = np.ma.masked_invalid(matrix)
    finite = matrix[np.isfinite(matrix)]
    if finite.size:
        vmin = min(float(finite.min()), 0.99)
        vmax = max(float(finite.max()), 1.01)
    else:
        vmin, vmax = 0.5, 1.5
    norm = TwoSlopeNorm(vmin=vmin, vcenter=1.0, vmax=vmax)
    cmap = plt.get_cmap('RdYlGn').copy()
    cmap.set_bad('lightgrey')
    im = ax.imshow(masked, cmap=cmap, norm=norm, aspect='auto')

    ax.set_xticks(range(len(_MAX_STEPS)))
    ax.set_xticklabels(_MAX_STEPS)
    ax.set_yticks(range(len(_MIN_DISTS)))
    ax.set_yticklabels(_MIN_DISTS)
    ax.set_xlabel('max_steps  (goal-region radius -> dispersion)')
    ax.set_ylabel('min_dist  (start -> goal-centre distance)')
    ax.set_title(title, fontsize=10, fontweight='bold')

    for i in range(len(_MIN_DISTS)):
        for j in range(len(_MAX_STEPS)):
            v = matrix[i, j]
            txt = '—' if not np.isfinite(v) else f'{v:.2f}'
            ax.text(j, i, txt, ha='center', va='center',
                    fontsize=8, color='black')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                 label='AGG / INC')


def _draw_marginals(ax_steps,
                    ax_dist,
                    ratios_by_mode: dict[str, pd.DataFrame]) -> None:
    """
    ============================================================================
     Draw the two main-effect marginals, eager and lazy overlaid:
       - left  : mean ratio vs max_steps (averaged over min_dist + maps).
       - right : mean ratio vs min_dist  (averaged over max_steps + maps).
    ============================================================================
    """
    for cfg, display, colour in _AGG_MODES:
        ratios = ratios_by_mode.get(cfg)
        if ratios is None or ratios.empty:
            continue
        by_steps = ratios.groupby('max_steps')['ratio'].mean()
        by_steps = by_steps.reindex(_MAX_STEPS)
        ax_steps.plot(by_steps.index, by_steps.values,
                      marker='o', color=colour, label=display)
        by_dist = ratios.groupby('min_dist')['ratio'].mean()
        by_dist = by_dist.reindex(_MIN_DISTS)
        ax_dist.plot(by_dist.index, by_dist.values,
                     marker='o', color=colour, label=display)

    for ax, xlabel in ((ax_steps, 'max_steps'), (ax_dist, 'min_dist')):
        ax.axhline(1.0, color='dimgray', linestyle='--', linewidth=1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel('mean AGG / INC')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8, framealpha=0.85)
    ax_steps.set_title('main effect: dispersion', fontsize=10)
    ax_dist.set_title('main effect: distance', fontsize=10)


def _plot_metric_page(pdf: PdfPages,
                      df_inc: pd.DataFrame,
                      df_agg: pd.DataFrame,
                      metric: str,
                      title: str) -> None:
    """
    ============================================================================
     One PDF page for `metric`: a heatmap per AGG mode (top) plus the two
     marginal main-effect plots (bottom).
    ============================================================================
    """
    fig = plt.figure(figsize=(13, 9.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 2], hspace=0.32,
                          wspace=0.28)
    fig.suptitle(f'AGG / INC phase diagram — {title}',
                 fontsize=13, fontweight='bold')

    ratios_by_mode: dict[str, pd.DataFrame] = {}
    for idx, (cfg, display, _colour) in enumerate(_AGG_MODES):
        df_cfg = df_agg[df_agg['config'] == cfg]
        ratios = _ratio_long(df_inc=df_inc, df_agg_cfg=df_cfg,
                             metric=metric)
        ratios_by_mode[cfg] = ratios
        matrix = _ratio_matrix(ratios=ratios)
        ax = fig.add_subplot(gs[0, idx])
        _draw_heatmap(ax=ax, matrix=matrix, title=display)

    ax_steps = fig.add_subplot(gs[1, 0])
    ax_dist = fig.add_subplot(gs[1, 1])
    _draw_marginals(ax_steps=ax_steps, ax_dist=ax_dist,
                    ratios_by_mode=ratios_by_mode)

    pdf.savefig(fig)
    plt.close(fig)


# ── Public API ─────────────────────────────────────────────────────────────

def make_heatmaps(path_drive_csv_inc: str,
                  path_drive_csv_agg: str,
                  path_drive_pdf_out: str) -> None:
    """
    ============================================================================
     Read the INC and AGG grid CSVs from Drive, derive `mem_total`, and
     write one phase-diagram page per headline metric to a multi-page PDF
     on Drive.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    df_inc = _download_csv(drive=drive, path=path_drive_csv_inc)
    df_agg = _download_csv(drive=drive, path=path_drive_csv_agg)

    for df in (df_inc, df_agg):
        df['mem_total'] = df['mem_open'] + df['mem_closed']

    n_inc_cells = df_inc[_KEYS].drop_duplicates().shape[0]
    n_maps = df_inc[['domain', 'map']].drop_duplicates().shape[0]
    _log.info(f'INC instances={n_inc_cells:,} across {n_maps} maps; '
              f'AGG rows={len(df_agg):,}')

    fd, path_pdf = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    try:
        with PdfPages(path_pdf) as pdf:
            for metric, title in _METRICS:
                _plot_metric_page(pdf=pdf,
                                  df_inc=df_inc,
                                  df_agg=df_agg,
                                  metric=metric,
                                  title=title)
        _log.info(f'wrote {path_pdf}')
        drive.upload(path_src=path_pdf,
                     path_dest=path_drive_pdf_out)
        _log.info(f'uploaded -> {path_drive_pdf_out}')
    finally:
        if os.path.exists(path_pdf):
            os.unlink(path_pdf)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    path_drive_csv_inc = (
        'Experiments/OMSPP/goal_distance/kastar_inc_grid.csv')
    path_drive_csv_agg = (
        'Experiments/OMSPP/goal_distance/kastar_agg_grid.csv')
    path_drive_pdf_out = (
        'Experiments/OMSPP/goal_distance/inc_vs_agg_phase.pdf')

    make_heatmaps(path_drive_csv_inc=path_drive_csv_inc,
                  path_drive_csv_agg=path_drive_csv_agg,
                  path_drive_pdf_out=path_drive_pdf_out)
    _log.info('--- done ---')
