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
   Load every *.map file from 2026/04/experiments/maps, run the core function
   with n = 1_000_000, steps = 10, min_cells = 10; write the CSV to
   2026/04/experiments/clusters/steps_10_min_cells_10.csv.

 Location rationale
   f_hs/experiments/clusters/ -- sits next to s_1_pair_clusters.py; layer
   boundary respected (f_ds stays I/O-free).

 Memory / size
   Fully streaming:
     - Grids are pulled from Drive one at a time via a generator and
       released when the next one is fetched (peak: ~1 grid in RAM).
     - Cluster samples are written row-by-row and discarded (peak: ~1
       row).
   Total peak memory is independent of both `len(grids)` and `n`.
===============================================================================
"""
import os
import csv
import tempfile
import logging
from typing import Iterable, Iterator

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, ClusterDiamond


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# CSV column order -- one source of truth for header and rows.
# DictWriter is created with extrasaction='ignore' below, so extra keys in
# Cluster.to_analytics() (rows, cols, n_cells_grid) are silently dropped.
_CSV_COLUMNS = [
    'domain',
    'map',
    'center_row',
    'center_col',
    'steps',
    'cells',
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _iter_grids_from_drive(drive: Drive,
                           path_drive_maps: str
                           ) -> Iterator[GridMap]:
    """
    ============================================================================
     Yield one GridMap at a time from the maps folder on Drive.
     The previous grid becomes unreachable once the next one is yielded,
     so peak memory stays at ~1 grid even when the folder has many maps.
    ============================================================================
    """
    paths = drive.filepaths(
        path=path_drive_maps,
        recursive=True,
        predicate=lambda name: name.endswith('.map'))
    _log.info(f'found {len(paths)} *.map files in '
              f'{path_drive_maps}')
    for path in paths:
        name = os.path.basename(path).removesuffix('.map')
        _log.info(f'  reading: {path}')
        content = drive.read(path=path).text
        grid = GridMap.From.text(content=content, name=name)
        _log.info(f'    -> {grid.name}: '
                  f'{grid.rows}x{grid.cols}, '
                  f'{len(grid):,} valid cells')
        yield grid


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
                writer.writerow(cluster.to_analytics())
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
    path_drive_maps = '2026/04/experiments/maps'
    steps = 10
    min_cells = 10
    n = 1_000
    path_drive_csv = (f'2026/04/experiments/clusters/'
                      f'steps_{steps}_min_cells_{min_cells}.csv')
    # Streaming loader: yields one grid at a time, releases on next.
    drive = Drive.Factory.valdas()
    _log.info(f'streaming grids from {path_drive_maps}')
    grids = _iter_grids_from_drive(drive=drive,
                                   path_drive_maps=path_drive_maps)
    # Run
    generate_cluster_samples(grids=grids,
                             path_drive_csv=path_drive_csv,
                             steps=steps,
                             min_cells=min_cells,
                             n=n)
    _log.info('--- done ---')
