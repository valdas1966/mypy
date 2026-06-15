"""
===============================================================================
 Utility: sample a POOL of candidate cluster locations from grid maps.

 A "cluster pool" is a set of ClusterDiamonds sampled at random across one
 or more GridMaps -- the candidate-location step shared by every grid-based
 heuristic-search experiment (MOSPP / OMSPP / MMSPP / goal_distance).

 The pool's CHARACTER is set by two params, not by separate scripts:
   - START pool : steps=0,  min_cells=1    -> single cells.
   - GOAL  pool : steps>=1, min_cells=k    -> sizeable regions (>= k cells,
                  so k goals can later be drawn from one).
 So the historical `s_0_clusters_start` and `s_1_clusters_goals` are the
 SAME operation invoked with different (steps, min_cells); this module is
 their shared home.
-------------------------------------------------------------------------------
 Two entry points (pure logic separated from Drive I/O):
   sample_pool(grids, steps, min_cells, n, max_tries) -> Iterator[dict]
       Pure core: yields one metadata row per sampled cluster.
       Unit-testable with an in-memory GridMap (no Drive).
   generate_pool_csv(path_drive_grids_pkl, path_drive_csv, ...) -> None
       Orchestration: read grids pickle -> sample_pool -> upload CSV.
       Drive plumbing (pickle / CSV / temp files) lives on `Drive`
       (`read_pickle`, `upload_rows`), not here.

 Reproducibility
   GridMap sampling draws from the PROCESS-GLOBAL `random` module
   (f_ds `GridMap.random.cells` -> `random.sample`). `generate_pool_csv`
   seeds via `random.seed(seed)` when `seed` is not None; pass a seed for
   reproducible pools. `sample_pool` does NOT seed -- the caller owns the
   global RNG (the _tester seeds explicitly).

 CSV schema (one row per sampled cluster):
   domain, map, center_row, center_col, steps, cells
===============================================================================
"""
import random
from typing import Iterable, Iterator

from f_log import get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, ClusterDiamond


_log = get_log(__name__)


# CSV column order -- one source of truth for the upload schema.
_CSV_COLUMNS = [
    'domain',
    'map',
    'center_row',
    'center_col',
    'steps',
    'cells',
]


# ── Pure sampler (no Drive) ──────────────────────────────────────────────────

def sample_pool(grids: Iterable[GridMap],
                steps: int,
                min_cells: int,
                n: int,
                max_tries: int = 100) -> Iterator[dict]:
    """
    ============================================================================
     For each grid in `grids`, sample up to `n` random ClusterDiamonds of
     Manhattan radius `steps`, each with at least `min_cells` cells, and
     yield one metadata row per successful sample. Samples that cannot
     reach `min_cells` within `max_tries` are skipped with a warning
     (sparse maze topologies may skip a few).

     `grids` is any iterable -- a list or a generator (peak memory ~one
     grid). Randomness is driven by the process-global `random` module;
     seed it before iterating for reproducible pools.

     Yields dicts with keys: domain, map, center_row, center_col, steps,
     cells.
    ============================================================================
    """
    for grid in grids:
        _log.info(f'  sampling {n:,} clusters on {grid.name} '
                  f'({grid.rows}x{grid.cols}, {len(grid):,} valid)')
        n_ok = 0
        n_fail = 0
        for i in range(n):
            try:
                cluster = ClusterDiamond.Factory.random(
                    grid=grid,
                    min_cells=min_cells,
                    steps=steps,
                    max_tries=max_tries)
            except ValueError as e:
                n_fail += 1
                _log.warning(f'    skip sample {i + 1}/{n} on '
                             f'{grid.name}: {e}')
                continue
            yield {
                'domain':     grid.domain,
                'map':        grid.name,
                'center_row': cluster.center.row,
                'center_col': cluster.center.col,
                'steps':      cluster.steps,
                'cells':      len(cluster),
            }
            n_ok += 1
        _log.info(f'    done: {n_ok:,}/{n:,} samples on '
                  f'{grid.name} ({n_fail} skipped)')


# ── Orchestration (Drive in, Drive out) ──────────────────────────────────────

def generate_pool_csv(path_drive_grids_pkl: str,
                      path_drive_csv: str,
                      steps: int,
                      min_cells: int,
                      n: int,
                      seed: int | None = None,
                      max_tries: int = 100,
                      drive: Drive | None = None) -> None:
    """
    ============================================================================
     Read the grids bundle from `path_drive_grids_pkl` on Drive, sample a
     cluster pool (`sample_pool`), and upload it as a CSV to
     `path_drive_csv` (schema: domain, map, center_row, center_col, steps,
     cells). The grids pickle may hold a `dict[str, GridMap]` or a
     `list[GridMap]`.

     `seed` -- pass an int for a reproducible pool (seeds the process-
     global `random` module). `drive` -- inject a Drive for tests / reuse;
     a VALDAS Drive is created when None.
    ============================================================================
    """
    _log.info(f'generate_pool_csv('
              f'grids_pkl={path_drive_grids_pkl}, '
              f'csv={path_drive_csv}, '
              f'steps={steps}, min_cells={min_cells}, n={n}, '
              f'seed={seed})')
    drive = drive if drive is not None else Drive.Factory.valdas()
    obj = drive.read_pickle(path=path_drive_grids_pkl)
    grids = list(obj.values()) if isinstance(obj, dict) else obj
    if seed is not None:
        random.seed(seed)
    rows = sample_pool(grids=grids,
                       steps=steps,
                       min_cells=min_cells,
                       n=n,
                       max_tries=max_tries)
    drive.upload_rows(rows=rows,
                      columns=_CSV_COLUMNS,
                      path=path_drive_csv)
    _log.info(f'uploaded csv -> {path_drive_csv}')
