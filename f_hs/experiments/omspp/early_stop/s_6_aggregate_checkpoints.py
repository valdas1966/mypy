"""
===============================================================================
 Script: aggregate the kA*-INC vs kA*-AGG mission-cancellation checkpoints
 into one tidy per-(algo, r) MEAN table on Drive.

 This is the data half of the early-stop story: a full k=200 OMSPP search
 is cancelled after r objectives complete; the runners (s_4 INC, s_5 AGG)
 price the cost incurred at each r. This script does NOT plot -- it groups
 their raw rows to a per-(algo, r) mean and persists that table. Reports
 (tex / pdf) are rendered on demand from this aggregate.

 The two series share one schema, so `algo` is the series key:
   inc  -- INC, incremental.
   agg  -- AGG, aggregative kA*-MIN (lazy, opt, stored vector).

 Pipeline (all via f_psl/pandas UDf): read inc + agg -> union -> group the
 metrics by (algo, r) with mean -> write. The AGG/INC memory ratio is
 derivable from `mem_total` at report time, so it is not stored here.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/early_stop/inc_checkpoints{suffix}.csv
   Experiments/OMSPP/early_stop/agg_checkpoints{suffix}.csv

 Output  (Drive)
   Experiments/OMSPP/early_stop/checkpoints_by_r{suffix}.csv
   columns: algo, r, cnt_expanded, mem_total, elapsed_total

 `suffix` is '' for full-run CSVs or '_toy{N}' for toy CSVs.
===============================================================================
"""
import os
import tempfile
import logging

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_psl.pandas.df import UDf


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# `algo` is the series key (inc / agg) -- one config each, no config col.
_GROUP_KEYS = ['algo', 'r']

# Metrics averaged over the (domain, map) pairs at each (algo, r).
_METRICS = ['cnt_expanded', 'mem_total', 'elapsed_total']


def aggregate_checkpoints(path_drive_inc_csv: str,
                          path_drive_agg_csv: str,
                          path_drive_out_csv: str) -> None:
    """
    ============================================================================
     Download the INC + AGG checkpoint CSVs, mean the metrics per
     (algo, r), and upload the tidy aggregate CSV to Drive.
    ============================================================================
    """
    drive = Drive.Factory.valdas()

    fd_inc, path_inc = tempfile.mkstemp(suffix='.csv')
    os.close(fd_inc)
    fd_agg, path_agg = tempfile.mkstemp(suffix='.csv')
    os.close(fd_agg)
    fd_out, path_out = tempfile.mkstemp(suffix='.csv')
    os.close(fd_out)

    try:
        _log.info(f'downloading {path_drive_inc_csv}')
        drive.download(path_src=path_drive_inc_csv, path_dest=path_inc)
        _log.info(f'downloading {path_drive_agg_csv}')
        drive.download(path_src=path_drive_agg_csv, path_dest=path_agg)

        df_inc = UDf.read(path=path_inc)
        df_agg = UDf.read(path=path_agg)
        _log.info(f'loaded: inc={len(df_inc):,} rows, '
                  f'agg={len(df_agg):,} rows')

        df_all = UDf.union(df_1=df_inc, df_2=df_agg)
        means = UDf.group(df=df_all,
                          col_a=_GROUP_KEYS,
                          col_b=_METRICS,
                          agg='mean')
        _log.info(f'aggregated -> {len(means):,} (algo, r) rows')

        UDf.write(df=means, path=path_out)
        drive.upload(path_src=path_out, path_dest=path_drive_out_csv)
        _log.info(f'uploaded aggregate -> {path_drive_out_csv}')

    finally:
        for path in (path_inc, path_agg, path_out):
            if os.path.exists(path):
                os.unlink(path)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Toy suffix must match the runner outputs ('' for full run).
    suffix = ''

    base = 'Experiments/OMSPP/early_stop'
    aggregate_checkpoints(
        path_drive_inc_csv=f'{base}/inc_checkpoints{suffix}.csv',
        path_drive_agg_csv=f'{base}/agg_checkpoints{suffix}.csv',
        path_drive_out_csv=f'{base}/checkpoints_by_r{suffix}.csv')
    _log.info('--- done ---')
