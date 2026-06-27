"""
===============================================================================
 Script: plot kA*-INC vs kA*-AGG mission-cancellation checkpoints as a
 multi-page PDF on Drive.

 The early-stop story: a full k=200 OMSPP search is cancelled after r
 objectives complete; we plot the cost incurred vs r. The headline is
 AGG's memory tax `|OPEN|*|A|` -- heaviest at small r (|A| ~ k) and
 decaying toward INC as r -> k (|A| -> k-r). INC's incremental
 1-h/node keeps a flat, light curve.

 Three series per metric chart:
   Incremental    -- inc_checkpoints.csv (algo='inc').      Black.
   AGG lazy_opt_sv   -- agg_checkpoints.csv.                Red.
   AGG lazy_opt_nosv -- agg_checkpoints.csv (mem contrast). Blue.

 X-axis: r (reach-rank of the completed goal), {1,50,100,150,199}.
 Y-axis: metric value, MEAN over the (domain, map) pairs at each r.

 Pages (per metric: chart on top, per-r mean table below):
   cnt_expanded, mem_total, elapsed_total,
   + a memory-ratio page (AGG/INC mem_total vs r) -- the headline curve.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/early_stop/inc_checkpoints{suffix}.csv
   Experiments/OMSPP/early_stop/agg_checkpoints{suffix}.csv

 Output  (Drive)
   Experiments/OMSPP/early_stop/checkpoints{suffix}.pdf

 `suffix` is '' for full-run CSVs or '_toy{N}' for toy CSVs.
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
from matplotlib.backends.backend_pdf import PdfPages

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Series label -> line style. INC plus the two AGG memory configs.
_SERIES_INC = 'Incremental'
_SERIES_AGG_SV = 'AGG lazy_opt_sv'
_SERIES_AGG_NOSV = 'AGG lazy_opt_nosv'

_SPECS: dict[str, dict] = {
    _SERIES_INC:      dict(color='black',    linewidth=2.6, marker='o'),
    _SERIES_AGG_SV:   dict(color='tab:red',  linewidth=2.2, marker='o'),
    _SERIES_AGG_NOSV: dict(color='tab:blue', linewidth=2.2, marker='s'),
}

# Metric -> (column, human title, y-axis label).
_METRICS: list[tuple[str, str, str]] = [
    ('cnt_expanded', 'Expanded nodes vs cancellation point',
     'mean expanded nodes'),
    ('mem_total', 'Peak memory (slot model) vs cancellation point',
     'mean peak slots  |CLOSED| + |OPEN|*(1+|A|)'),
    ('elapsed_total', 'Runtime vs cancellation point',
     'mean elapsed (s)'),
]

_RS = [1, 50, 100, 150, 199]


# ── Data assembly ────────────────────────────────────────────────────────────

def _series_frames(df_inc: pd.DataFrame,
                   df_agg: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    ========================================================================
     Split the two CSVs into one frame per plotted series, keyed by the
     series label. AGG splits on its `config` column.
    ========================================================================
    """
    return {
        _SERIES_INC:      df_inc,
        _SERIES_AGG_SV:   df_agg[df_agg['config'] == 'lazy_opt_sv'],
        _SERIES_AGG_NOSV: df_agg[df_agg['config'] == 'lazy_opt_nosv'],
    }


def _mean_by_r(frame: pd.DataFrame, column: str) -> pd.Series:
    """
    ========================================================================
     Mean of `column` over (domain, map) at each r, indexed by r in
     _RS order.
    ========================================================================
    """
    means = frame.groupby('r')[column].mean()
    return means.reindex(_RS)


# ── Page drawing ─────────────────────────────────────────────────────────────

def _draw_metric_page(pdf: PdfPages,
                      frames: dict[str, pd.DataFrame],
                      column: str,
                      title: str,
                      ylabel: str) -> None:
    """
    ========================================================================
     One page: line chart (top) of the metric vs r for each series,
     and a per-r mean table (bottom).
    ========================================================================
    """
    fig, (ax, ax_tbl) = plt.subplots(
        2, 1, figsize=(8.5, 11),
        gridspec_kw=dict(height_ratios=[3, 2]))

    table_cols: list[list[str]] = []
    for label, frame in frames.items():
        means = _mean_by_r(frame, column)
        spec = _SPECS[label]
        ax.plot(_RS, means.values, label=label, markersize=5, **spec)
        table_cols.append([f'{v:,.1f}' if pd.notna(v) else '-'
                           for v in means.values])

    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('r  (completed objectives at cancellation)')
    ax.set_ylabel(ylabel)
    ax.set_xticks(_RS)
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax_tbl.axis('off')
    cell_text = list(map(list, zip(*table_cols)))   # transpose -> rows=r
    tbl = ax_tbl.table(
        cellText=cell_text,
        rowLabels=[f'r={r}' for r in _RS],
        colLabels=list(frames.keys()),
        loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)

    pdf.savefig(fig)
    plt.close(fig)


def _draw_ratio_page(pdf: PdfPages,
                     frames: dict[str, pd.DataFrame]) -> None:
    """
    ========================================================================
     Headline page: AGG / INC peak-memory ratio vs r. Shows the AGG tax
     decaying from its small-r peak toward 1.0 as r -> k.
    ========================================================================
    """
    fig, ax = plt.subplots(figsize=(8.5, 6))
    inc = _mean_by_r(frames[_SERIES_INC], 'mem_total')

    for label in (_SERIES_AGG_SV, _SERIES_AGG_NOSV):
        agg = _mean_by_r(frames[label], 'mem_total')
        ratio = agg.values / inc.values
        spec = dict(_SPECS[label])
        ax.plot(_RS, ratio, label=f'{label} / INC', markersize=5, **spec)

    ax.axhline(1.0, color='gray', linestyle='--', linewidth=1)
    ax.set_title('AGG / INC peak-memory ratio vs cancellation point',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('r  (completed objectives at cancellation)')
    ax.set_ylabel('peak-slot ratio  (AGG / INC)')
    ax.set_xticks(_RS)
    ax.grid(True, alpha=0.3)
    ax.legend()

    pdf.savefig(fig)
    plt.close(fig)


# ── Public API ───────────────────────────────────────────────────────────────

def make_checkpoint_plots(path_drive_inc_csv: str,
                          path_drive_agg_csv: str,
                          path_drive_pdf_out: str) -> None:
    """
    ============================================================================
     Download the INC + AGG checkpoint CSVs, build the per-metric pages
     plus the memory-ratio headline page, and upload the PDF to Drive.
    ============================================================================
    """
    drive = Drive.Factory.valdas()

    fd_inc, path_inc = tempfile.mkstemp(suffix='.csv')
    os.close(fd_inc)
    fd_agg, path_agg = tempfile.mkstemp(suffix='.csv')
    os.close(fd_agg)
    fd_pdf, path_pdf = tempfile.mkstemp(suffix='.pdf')
    os.close(fd_pdf)

    try:
        _log.info(f'downloading {path_drive_inc_csv}')
        drive.download(path_src=path_drive_inc_csv, path_dest=path_inc)
        _log.info(f'downloading {path_drive_agg_csv}')
        drive.download(path_src=path_drive_agg_csv, path_dest=path_agg)

        df_inc = pd.read_csv(path_inc)
        df_agg = pd.read_csv(path_agg)
        _log.info(f'loaded: inc={len(df_inc):,} rows, '
                  f'agg={len(df_agg):,} rows')

        frames = _series_frames(df_inc=df_inc, df_agg=df_agg)

        with PdfPages(path_pdf) as pdf:
            for column, title, ylabel in _METRICS:
                _draw_metric_page(pdf=pdf, frames=frames, column=column,
                                  title=title, ylabel=ylabel)
            _draw_ratio_page(pdf=pdf, frames=frames)

        drive.upload(path_src=path_pdf, path_dest=path_drive_pdf_out)
        _log.info(f'uploaded pdf -> {path_drive_pdf_out}')

    finally:
        for path in (path_inc, path_agg, path_pdf):
            if os.path.exists(path):
                os.unlink(path)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Toy suffix must match the runner outputs ('' for full run).
    suffix = ''

    base = 'Experiments/OMSPP/early_stop'
    make_checkpoint_plots(
        path_drive_inc_csv=f'{base}/inc_checkpoints{suffix}.csv',
        path_drive_agg_csv=f'{base}/agg_checkpoints{suffix}.csv',
        path_drive_pdf_out=f'{base}/checkpoints{suffix}.pdf')
    _log.info('--- done ---')
