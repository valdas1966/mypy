"""
===============================================================================
 Script: generate PairClusters for every map in a Google Drive folder,
 then upload the result as a pickle (the full PairClusters, for later
 experiment re-use) and a CSV (flat metadata, for analysis).
-------------------------------------------------------------------------------
 Input
   path_drive_maps:  Drive folder containing *.map files.
   n_pairs:          Number of PairClusters to generate per map.
   min_dist:         Minimum Manhattan distance between cluster centers.
   steps_a:          Manhattan radius of cluster A.
   min_cells_a:      Minimum valid cells required in cluster A.
   steps_b:          Manhattan radius of cluster B.
   min_cells_b:      Minimum valid cells required in cluster B.
   path_drive_out:   Drive folder to upload `<name_out>.pkl` and
                     `<name_out>.csv` to.
   name_out:         Base filename (without extension) for both outputs.

 Output
   (a) In-memory:    dict[map_name -> list[PairCluster]]
   (b) Drive:
         path_drive_out/<name_out>.pkl   (full PairClusters)
         path_drive_out/<name_out>.csv   (one row per pair)

 Location rationale
   f_hs/experiments/clusters/. Generator is problem-family-agnostic:
     min_cells_a = min_cells_b = 1  -> SPP instance
     min_cells_a = 1, min_cells_b > 1  -> OMSPP instance
     min_cells_a > 1, min_cells_b = 1  -> MOSPP instance
     min_cells_a > 1, min_cells_b > 1  -> MMSPP instance
===============================================================================
"""
import os
import csv
import tempfile
import logging

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, PairCluster
from f_utils import u_pickle


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_grid_from_drive(drive: Drive, path_drive: str) -> GridMap:
    """
    ============================================================================
     Download a .map file from Drive to a temp path, build a GridMap, remove
     the temp file, and return the grid.
    ============================================================================
    """
    file_name = os.path.basename(path_drive)
    map_name = file_name.removesuffix('.map')
    _log.info(f'  load map: {path_drive}')
    # Download to temp
    tmp = tempfile.NamedTemporaryFile(suffix='.map', delete=False)
    tmp.close()
    path_local = tmp.name
    try:
        drive.download(path_src=path_drive, path_dest=path_local)
        grid = GridMap.From.file_map(path=path_local, name=map_name)
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)
    _log.info(f'    -> {grid.name}: '
              f'{grid.rows}x{grid.cols}, '
              f'{len(grid)} valid cells')
    return grid


def _pair_clusters_for_grid(grid: GridMap,
                            n_pairs: int,
                            min_dist: int,
                            steps_a: int,
                            min_cells_a: int,
                            steps_b: int,
                            min_cells_b: int,
                            max_tries: int
                            ) -> list[PairCluster]:
    """
    ============================================================================
     Generate n_pairs PairClusters on a single grid.
    ============================================================================
    """
    _log.info(f'  sample {n_pairs} pairs on {grid.name}')
    pairs: list[PairCluster] = []
    for i in range(n_pairs):
        pair = PairCluster.Factory.random(
            grid=grid,
            min_cells_a=min_cells_a,
            min_cells_b=min_cells_b,
            steps_a=steps_a,
            steps_b=steps_b,
            min_distance=min_dist,
            max_tries=max_tries)
        pairs.append(pair)
        _log.debug(f'    pair {i+1}/{n_pairs}: {pair}')
    _log.info(f'    -> {len(pairs)} pairs '
              f'(distances: '
              f'min={min(p.distance for p in pairs)}, '
              f'max={max(p.distance for p in pairs)})')
    return pairs


def _save_pickle_to_drive(drive: Drive,
                          obj,
                          path_drive_out: str,
                          name_out: str) -> None:
    """
    ============================================================================
     Dump `obj` with u_pickle to a temp file, upload to
     `<path_drive_out>/<name_out>.pkl`, remove temp.
    ============================================================================
    """
    path_drive_pkl = f'{path_drive_out}/{name_out}.pkl'
    tmp = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
    tmp.close()
    path_local = tmp.name
    try:
        u_pickle.dump(obj, path_local)
        drive.upload(path_src=path_local, path_dest=path_drive_pkl)
        _log.info(f'uploaded pickle -> {path_drive_pkl}')
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)


# CSV column order -- shared between the header and the row-writer so the
# two can never drift out of sync.
_CSV_COLUMNS = [
    'map',
    'domain',
    'rows',
    'cols',
    'n_cells_grid',
    'pair_id',
    'center_a_row',
    'center_a_col',
    'center_b_row',
    'center_b_col',
    'steps_a',
    'steps_b',
    'n_cells_a',
    'n_cells_b',
    'distance',
]


def _save_csv_to_drive(drive: Drive,
                       pairs_by_map: dict[str, list[PairCluster]],
                       path_drive_out: str,
                       name_out: str) -> None:
    """
    ============================================================================
     Build a CSV with one row per PairCluster (metadata via to_analytics())
     and upload to `<path_drive_out>/<name_out>.csv`.
    ============================================================================
    """
    path_drive_csv = f'{path_drive_out}/{name_out}.csv'
    tmp = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local = tmp.name
    try:
        writer = csv.DictWriter(tmp, fieldnames=_CSV_COLUMNS)
        writer.writeheader()
        for map_name, pairs in pairs_by_map.items():
            for pair_id, pair in enumerate(pairs):
                row = pair.to_analytics()
                row['pair_id'] = pair_id
                writer.writerow(row)
        tmp.close()
        drive.upload(path_src=path_local, path_dest=path_drive_csv)
        _log.info(f'uploaded csv    -> {path_drive_csv}')
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Public API ──────────────────────────────────────────────────────────────

def generate_pair_clusters(path_drive_maps: str,
                           n_pairs: int,
                           min_dist: int,
                           steps_a: int,
                           min_cells_a: int,
                           steps_b: int,
                           min_cells_b: int,
                           path_drive_out: str,
                           name_out: str = 'pair_clusters',
                           max_tries: int = 100
                           ) -> dict[str, list[PairCluster]]:
    """
    ============================================================================
     Read every *.map file from the given Drive folder, build a GridMap, and
     sample n_pairs PairClusters per grid. Upload both:
       (a) <name_out>.pkl --- dict[str, list[PairCluster]] (pickle).
       (b) <name_out>.csv --- flat per-pair metadata (one row per pair).
     Returns the in-memory dict for downstream use.
    ============================================================================
    """
    _log.info(f'generate_pair_clusters(path={path_drive_maps}, '
              f'n_pairs={n_pairs}, min_dist={min_dist}, '
              f'steps_a={steps_a}, min_cells_a={min_cells_a}, '
              f'steps_b={steps_b}, min_cells_b={min_cells_b}, '
              f'out={path_drive_out}/{name_out}.(pkl|csv))')
    drive = Drive.Factory.valdas()
    files = drive.files(path=path_drive_maps)
    map_files = [f for f in files if f.endswith('.map')]
    _log.info(f'found {len(map_files)} *.map files in '
              f'{path_drive_maps}')
    result: dict[str, list[PairCluster]] = {}
    for file_name in map_files:
        path_file = f'{path_drive_maps}/{file_name}'
        grid = _load_grid_from_drive(drive=drive,
                                     path_drive=path_file)
        pairs = _pair_clusters_for_grid(
            grid=grid,
            n_pairs=n_pairs,
            min_dist=min_dist,
            steps_a=steps_a,
            min_cells_a=min_cells_a,
            steps_b=steps_b,
            min_cells_b=min_cells_b,
            max_tries=max_tries)
        result[grid.name] = pairs
    _log.info(f'generated {len(result)} maps, '
              f'{sum(len(v) for v in result.values())} pairs total')
    _save_pickle_to_drive(drive=drive,
                          obj=result,
                          path_drive_out=path_drive_out,
                          name_out=name_out)
    _save_csv_to_drive(drive=drive,
                       pairs_by_map=result,
                       path_drive_out=path_drive_out,
                       name_out=name_out)
    return result


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters
    path_drive_maps = '2026/04/experiments/maps'
    path_drive_out = '2026/04/experiments/mospp'
    name_out = 'pair_clusters'
    n_pairs = 10
    min_dist = 100
    steps_a = 10
    min_cells_a = 10
    steps_b = 10
    min_cells_b = 10
    # Run
    pairs_by_map = generate_pair_clusters(
        path_drive_maps=path_drive_maps,
        n_pairs=n_pairs,
        min_dist=min_dist,
        steps_a=steps_a,
        min_cells_a=min_cells_a,
        steps_b=steps_b,
        min_cells_b=min_cells_b,
        path_drive_out=path_drive_out,
        name_out=name_out)
    # Summary
    _log.info('--- summary ---')
    for name, pairs in pairs_by_map.items():
        _log.info(f'{name}: {len(pairs)} pairs')
