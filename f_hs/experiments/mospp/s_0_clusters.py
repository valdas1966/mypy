"""
===============================================================================
 Script: sample N random ClusterDiamonds per GridMap, stream the metadata to
 a single CSV, and upload the CSV to Google Drive.
-------------------------------------------------------------------------------
 Core function (general)
   generate_cluster_samples(grids, path_drive_csv,
                            steps, min_cells, n,
                            max_tries=100) -> None

 __main__ (user's specific use case)
   Load all grids from a single pickle on Drive at
   2026/04/experiments/maps/grids/grids.pkl (each grid carries its
   `domain` attribute), run the core function with n = 1_000, steps = 10,
   min_cells = 10; write the CSV to
   2026/04/experiments/mospp/i_0_clusters.csv.

 Memory / size
   - Grids are loaded from a single pickle once; iterated and released
     in turn (peak grid count = whatever the pickle holds, but typically
     small — a few maps).
   - Cluster samples are written row-by-row and discarded (peak: ~1 row).
===============================================================================
"""
import os
import csv
import pickle
import tempfile
import logging
from typing import Iterable

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, ClusterDiamond


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'center_row',
    'center_col',
    'steps',
    'cells',
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_grids_from_pickle(drive: Drive,
                            path_drive_pkl: str
                            ) -> list[GridMap]:
    """
    ============================================================================
     Download the grids pickle from Drive and return the contained
     GridMaps as a list. The pickle is expected to hold either a
     `dict[str, GridMap]` (canonical, matching ProblemGrid.Store) or a
     plain `list[GridMap]`. Each grid carries its own `domain` attribute
     -- the whole point of switching to the pickled bundle.
    ============================================================================
    """
    _log.info(f'reading grids pickle: {path_drive_pkl}')
    # `drive.read` decodes as text; pickle is binary, so download to
    # a temp file and unpickle from disk.
    tmp = tempfile.NamedTemporaryFile(
        suffix='.pkl', delete=False, mode='wb')
    path_local = tmp.name
    tmp.close()
    try:
        drive.download(path_src=path_drive_pkl,
                       path_dest=path_local)
        with open(path_local, 'rb') as f:
            obj = pickle.load(f)
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)
    if isinstance(obj, dict):
        grids = list(obj.values())
    elif isinstance(obj, list):
        grids = obj
    else:
        raise TypeError(
            f'expected dict[str, GridMap] or list[GridMap] in '
            f'{path_drive_pkl}; got {type(obj).__name__}')
    for g in grids:
        _log.info(f'  loaded: {g.name} '
                  f'(domain={g.domain!r}, '
                  f'{g.rows}x{g.cols}, '
                  f'{len(g):,} valid cells)')
    return grids


# ── Public API ──────────────────────────────────────────────────────────────

def generate_cluster_samples(grids: Iterable[GridMap],
                             path_drive_csv: str,
                             steps: int,
                             min_cells: int,
                             n: int,
                             max_tries: int = 100) -> None:
    """
    ============================================================================
     For each grid in `grids`, sample n random ClusterDiamonds and stream
     their metadata to a single CSV file on Google Drive at `path_drive_csv`.

     `grids` is any iterable -- a list or a generator. When a generator is
     passed (recommended for large map sets), each GridMap is consumed one
     at a time and released before the next is fetched; peak memory stays
     at ~one grid.

     One row per sample. Columns:
       domain, map, center_row, center_col, steps, cells.
    ============================================================================
    """
    _log.info(f'generate_cluster_samples('
              f'path_drive_csv={path_drive_csv}, '
              f'steps={steps}, min_cells={min_cells}, n={n})')
    drive = Drive.Factory.valdas()
    tmp = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local = tmp.name
    try:
        writer = csv.DictWriter(tmp,
                                fieldnames=_CSV_COLUMNS,
                                extrasaction='ignore')
        writer.writeheader()
        for grid in grids:
            _log.info(f'  sampling {n:,} clusters on '
                      f'{grid.name} '
                      f'({grid.rows}x{grid.cols}, '
                      f'{len(grid):,} valid)')
            for i in range(n):
                cluster = ClusterDiamond.Factory.random(
                    grid=grid,
                    min_cells=min_cells,
                    steps=steps,
                    max_tries=max_tries)
                writer.writerow({
                    'domain':     grid.domain,
                    'map':        grid.name,
                    'center_row': cluster.center.row,
                    'center_col': cluster.center.col,
                    'steps':      cluster.steps,
                    'cells':      len(cluster),
                })
                if (i + 1) % 100_000 == 0:
                    _log.info(f'    {i + 1:,}/{n:,} '
                              f'sampled on {grid.name}')
            _log.info(f'    done: {n:,} samples on '
                      f'{grid.name}')
        tmp.close()
        drive.upload(path_src=path_local,
                     path_dest=path_drive_csv)
        _log.info(f'uploaded csv -> {path_drive_csv}')
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters
    path_drive_pkl = '2026/04/experiments/grids/grids.pkl'
    steps = 10
    min_cells = 10
    n = 100
    path_drive_csv = '2026/04/experiments/mospp/i_0_clusters.csv'
    # Load all grids from a single pickle on Drive.
    drive = Drive.Factory.valdas()
    grids = _load_grids_from_pickle(drive=drive,
                                    path_drive_pkl=path_drive_pkl)
    # Run
    generate_cluster_samples(grids=grids,
                             path_drive_csv=path_drive_csv,
                             steps=steps,
                             min_cells=min_cells,
                             n=n)
    _log.info('--- done ---')
