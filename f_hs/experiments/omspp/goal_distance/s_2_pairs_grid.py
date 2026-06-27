"""
===============================================================================
 goal_distance step s_2 -- build the per-map GEOMETRIC SKELETON for the
 (min_dist x max_steps) phase-diagram grid.

 Unlike the parent OMSPP s_2 (which RANDOM-samples start/goal pairs and
 filters by a min_dist floor), this variant builds the geometry
 DETERMINISTICALLY -- a "deterministic ray" controlled design:

   - One START per map: the valid cell nearest the top-left corner
     (row-major first valid) -- maximizes the south-east room the ray
     needs.
   - Five GOAL CENTERS per map: one per min_dist band {100..500}, placed
     due SOUTH-EAST of the start at EXACT Manhattan distance = the band
     value (ideal diagonal cell (start + d/2, start + d/2); if that cell
     is a wall, the nearest in-bounds valid cell on the same SE
     anti-diagonal within a small window is used, keeping the distance
     exact and the bearing ~SE).

 So across a map the start and the five goal centers are PINNED. The
 downstream s_3 keeps each center fixed and only grows the goal-region
 radius (max_steps) -- giving 5 (min_dist) x 5 (max_steps) = 25 instances
 per map, all sharing one fixed geometric skeleton. min_dist selects WHICH
 pinned goal center; max_steps selects the region radius.

 A band is SKIPPED (one fewer row, coverage made explicit in the log)
 when the map is too small to host a due-SE center at that distance, or
 walls block the whole search window. Map-size thinning at the far bands
 is reported, never hidden.

   in:  Experiments/Grids/grids.pkl       (name -> GridMap bundle)
   out: Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv
        one row per (map, min_dist) skeleton entry.
===============================================================================
"""
import logging

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, CellMap


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Phase-diagram distance axis (Manhattan, start -> goal center).
_MIN_DISTS = [100, 200, 300, 400, 500]

# Half-width (cells) of the SE anti-diagonal search window used to dodge
# a wall on the ideal diagonal cell while staying ~due-SE.
_RAY_WINDOW = 50

# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'start_row',
    'start_col',
    'goal_center_row',
    'goal_center_col',
    'min_dist',
    'dist',
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_grids(drive: Drive, path_drive_pkl: str) -> list[GridMap]:
    """
    ============================================================================
     Read the grids bundle pickle from Drive and return a list[GridMap].
     The bundle is a dict[name -> GridMap] (canonical) or a list[GridMap].
    ============================================================================
    """
    _log.info(f'reading grids pickle: {path_drive_pkl}')
    obj = drive.read_pickle(path=path_drive_pkl)
    if isinstance(obj, dict):
        grids = list(obj.values())
    elif isinstance(obj, list):
        grids = obj
    else:
        raise TypeError(
            f'expected dict[str, GridMap] or list[GridMap] in '
            f'{path_drive_pkl}; got {type(obj).__name__}')
    for g in grids:
        _log.info(f'  loaded: {g.name} (domain={g.domain!r}, '
                  f'{g.rows}x{g.cols}, {len(g):,} valid cells)')
    return grids


def _find_start(grid: GridMap) -> CellMap | None:
    """
    ============================================================================
     Return the valid cell nearest the top-left corner (row-major first
     valid). Anchoring the start there maximizes the south-east room the
     deterministic ray needs. None if the grid has no valid cell.
    ============================================================================
    """
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid[r][c]
            if cell:
                return cell
    return None


def _ray_center(grid: GridMap,
                start: CellMap,
                dist: int) -> CellMap | None:
    """
    ============================================================================
     Return the goal center for one min_dist band: the cell due SOUTH-EAST
     of `start` at EXACT Manhattan distance `dist`. The ideal cell is the
     diagonal midpoint (start_row + dist/2, start_col + dist/2). If that
     cell is out of bounds, the map is too small for a due-SE center at
     this distance -> None (band skipped). If it is in bounds but a wall,
     the nearest in-bounds VALID cell on the same SE anti-diagonal (cells
     at exact distance `dist`) within +/- `_RAY_WINDOW` of the midpoint is
     returned -- keeping the distance exact and the bearing ~SE. None if
     the whole window is blocked.
    ============================================================================
    """
    half = dist // 2
    ideal_row = start.row + half
    ideal_col = start.col + half
    # Out of bounds at the midpoint => map too small for a due-SE center.
    if not (0 <= ideal_row < grid.rows and 0 <= ideal_col < grid.cols):
        return None
    # Walk the SE anti-diagonal outward from the midpoint, nearest first.
    for delta in range(_RAY_WINDOW + 1):
        for a in {half - delta, half + delta}:
            if not 0 <= a <= dist:
                continue
            r = start.row + a
            c = start.col + (dist - a)
            if 0 <= r < grid.rows and 0 <= c < grid.cols:
                cell = grid[r][c]
                if cell:
                    return cell
    return None


def _skeleton_rows(grids: list[GridMap]) -> list[dict]:
    """
    ============================================================================
     Build the skeleton rows for every grid: one fixed start + up to five
     pinned goal centers (one per min_dist band). Bands with no feasible
     due-SE center are skipped with a warning so per-map coverage is
     explicit. Returns the list of CSV row dicts.
    ============================================================================
    """
    rows: list[dict] = []
    for grid in grids:
        start = _find_start(grid=grid)
        if start is None:
            _log.warning(f'  skip {grid.name}: no valid cell')
            continue
        n_ok = 0
        for dist in _MIN_DISTS:
            center = _ray_center(grid=grid, start=start, dist=dist)
            if center is None:
                _log.warning(f'  {grid.name}: min_dist={dist} skipped '
                             f'(no due-SE center fits)')
                continue
            realized = start.distance(center)
            rows.append({
                'domain':          grid.domain,
                'map':             grid.name,
                'start_row':       start.row,
                'start_col':       start.col,
                'goal_center_row': center.row,
                'goal_center_col': center.col,
                'min_dist':        dist,
                'dist':            realized,
            })
            n_ok += 1
        _log.info(f'  {grid.name}: start=({start.row},{start.col}), '
                  f'{n_ok}/{len(_MIN_DISTS)} bands placed')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def generate_pairs_grid(path_drive_grids_pkl: str,
                        path_drive_csv_out: str) -> None:
    """
    ============================================================================
     Read the grids bundle from `path_drive_grids_pkl`, build the
     deterministic-ray skeleton (one start + up to five pinned goal
     centers per map), and upload it as a CSV to `path_drive_csv_out`.

     One row per (map, min_dist) skeleton entry. Columns:
       domain, map, start_row, start_col,
       goal_center_row, goal_center_col, min_dist, dist.

     `min_dist` is the band label; `dist` is the realized Manhattan
     distance start -> goal center (== `min_dist` by construction, kept
     as a sanity column).
    ============================================================================
    """
    _log.info(f'generate_pairs_grid('
              f'grids_pkl={path_drive_grids_pkl}, '
              f'out={path_drive_csv_out})')
    drive = Drive.Factory.valdas()
    grids = _load_grids(drive=drive, path_drive_pkl=path_drive_grids_pkl)
    rows = _skeleton_rows(grids=grids)
    drive.upload_rows(rows=rows,
                      columns=_CSV_COLUMNS,
                      path=path_drive_csv_out)
    _log.info(f'uploaded csv -> {path_drive_csv_out} '
              f'({len(rows):,} skeleton rows across {len(grids)} maps)')


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters -- goal_distance step s_2: build the fixed geometric
    # skeleton (1 start + 5 due-SE goal centers per map) for the
    # min_dist x max_steps phase diagram. No RNG -- the geometry is
    # deterministic per the ray design.
    path_drive_grids_pkl = 'Experiments/Grids/grids.pkl'
    path_drive_csv_out = (
        'Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv')
    # Run
    generate_pairs_grid(path_drive_grids_pkl=path_drive_grids_pkl,
                        path_drive_csv_out=path_drive_csv_out)
    _log.info('--- done ---')
