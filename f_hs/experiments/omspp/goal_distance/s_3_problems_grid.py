"""
===============================================================================
 goal_distance step s_3 -- cross-join the fixed skeleton (s_2) with the
 max_steps axis to emit the full (min_dist x max_steps) problem grid:
 25 OMSPP ProblemGrids per map, k = 200 goals each.

 For every skeleton row (a PINNED start + PINNED goal center at one
 min_dist band) and every max_steps in {20,30,40,50,60}:
   - rebuild the GOAL ClusterDiamond at that radius around the pinned
     center (the center never moves -- only the region grows),
   - wrap (start_diamond, goal_diamond) in a PairCluster and log
     dist_start = pair.distance()  (P1 -- start -> goal-center distance),
   - draw k = 200 goals from the region,
   - build one ProblemGrid,
   - log dist_goals = mean pairwise goal distance (P2 -- realized
     dispersion) and region_cells (so saturation / thinning is visible).

 Because the region grows with max_steps, the 200 goals are RE-DRAWN per
 radius (a larger, more dispersed cloud) -- the intended manipulation of
 the spread axis at fixed k. A single shared, seeded RNG over a stable
 (map, min_dist, max_steps) iteration order makes the draws reproducible.

 A (min_dist, max_steps) cell is SKIPPED with a warning when the rebuilt
 region holds fewer than k cells (coverage made explicit, never hidden).

   in:   Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv  (skeleton)
         Experiments/Grids/grids.pkl                         (GridMaps)
   out:  Experiments/OMSPP/goal_distance/i_3_problems_grid.pkl
         Experiments/OMSPP/goal_distance/i_3_problems_grid.csv
   k = 200, max_steps = [20,30,40,50,60], seed = 0.
===============================================================================
"""
import csv
import random
import logging
from collections import defaultdict
from typing import NamedTuple

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, ClusterDiamond, PairCluster
from f_hs.problem.i_1_grid import ProblemGrid


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Goal-region radius axis (Manhattan steps from the pinned center).
_MAX_STEPS = [20, 30, 40, 50, 60]

# Goals per problem -- fixed across the whole grid.
_K = 200

# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'min_dist',
    'rep',
    'max_steps',
    'k',
    'dist_start',
    'dist_goals',
    'region_cells',
]


class _SkeletonRow(NamedTuple):
    """Per-row record parsed from the s_2 skeleton CSV."""
    domain: str
    map: str
    start_row: int
    start_col: int
    goal_center_row: int
    goal_center_col: int
    min_dist: int
    rep: int


# ── Helpers ────────────────────────────────────────────────────────────────

def _read_skeleton_grouped(drive: Drive,
                           path_drive_csv: str
                           ) -> dict[tuple[str, str], list[_SkeletonRow]]:
    """
    ============================================================================
     Download the s_2 skeleton CSV from Drive, parse it, and group rows by
     (domain, map). On-disk order is preserved within each group.
    ============================================================================
    """
    _log.info(f'reading {path_drive_csv}')
    text = drive.read(path=path_drive_csv).text
    reader = csv.DictReader(text.splitlines())
    groups: dict[tuple[str, str], list[_SkeletonRow]] = defaultdict(list)
    for row in reader:
        rec = _SkeletonRow(
            domain=row.get('domain', '') or '',
            map=row['map'],
            start_row=int(row['start_row']),
            start_col=int(row['start_col']),
            goal_center_row=int(row['goal_center_row']),
            goal_center_col=int(row['goal_center_col']),
            min_dist=int(row['min_dist']),
            rep=int(row['rep']),
        )
        groups[(rec.domain, rec.map)].append(rec)
    total = sum(len(rs) for rs in groups.values())
    _log.info(f'  loaded {total:,} skeleton rows across '
              f'{len(groups)} (domain, map) groups')
    return groups


def _load_grids_by_name(drive: Drive,
                        path_drive_pkl: str) -> dict[str, GridMap]:
    """
    ============================================================================
     Download the grids bundle pickle and return a name -> GridMap map.
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
    by_name: dict[str, GridMap] = {}
    for g in grids:
        _log.info(f'  loaded: {g.name} (domain={g.domain!r}, '
                  f'{g.rows}x{g.cols}, {len(g):,} valid cells)')
        by_name[g.name] = g
    return by_name


def _mean_pairwise(rcs: list[tuple[int, int]]) -> float:
    """
    ============================================================================
     Mean pairwise Manhattan distance among the (row, col) goals (0 when
     fewer than two goals). Realized goal dispersion -- the P2 axis.
    ============================================================================
    """
    if len(rcs) < 2:
        return 0.0
    n_pairs = len(rcs) * (len(rcs) - 1) // 2
    total = 0
    for i in range(len(rcs)):
        ri, ci = rcs[i]
        for j in range(i + 1, len(rcs)):
            rj, cj = rcs[j]
            total += abs(ri - rj) + abs(ci - cj)
    return total / n_pairs


def _build_instance(grid: GridMap,
                    rec: _SkeletonRow,
                    max_steps: int,
                    rng: random.Random,
                    ) -> tuple[ProblemGrid, dict] | None:
    """
    ============================================================================
     Build one (min_dist, max_steps) instance from a skeleton row:
     rebuild the goal ClusterDiamond at `max_steps` around the pinned
     center, draw k goals, and return (ProblemGrid, meta_row). Returns
     None (skip) when the rebuilt region holds fewer than k cells.

     dist_start (P1) is read off a PairCluster(start_diamond, goal_diamond)
     -- the start is a steps=0 single-cell diamond, the goal is the
     radius-`max_steps` region; pair.distance() is their center-to-center
     Manhattan distance.
    ============================================================================
    """
    start_cell = grid[rec.start_row][rec.start_col]
    goal_center = grid[rec.goal_center_row][rec.goal_center_col]
    start_diamond = ClusterDiamond(grid=grid, center=start_cell, steps=0)
    goal_diamond = ClusterDiamond(grid=grid,
                                  center=goal_center,
                                  steps=max_steps)
    region_cells = len(goal_diamond)
    if region_cells < _K:
        _log.warning(f'  {grid.name}: min_dist={rec.min_dist}, '
                     f'max_steps={max_steps} skipped '
                     f'(region {region_cells} < k={_K})')
        return None
    pair = PairCluster(cluster_a=start_diamond, cluster_b=goal_diamond)
    dist_start = pair.distance()
    goals = rng.sample(list(goal_diamond), k=_K)
    name = (f'{grid.name}_d{rec.min_dist:03d}'
            f'_r{rec.rep:02d}_s{max_steps:02d}')
    problem = ProblemGrid(grid=grid,
                          starts=[start_cell],
                          goals=goals,
                          name=name)
    dist_goals = _mean_pairwise(rcs=problem.goals_rc)
    meta = {
        'domain':       rec.domain,
        'map':          grid.name,
        'min_dist':     rec.min_dist,
        'rep':          rec.rep,
        'max_steps':    max_steps,
        'k':            _K,
        'dist_start':   dist_start,
        'dist_goals':   round(dist_goals, 4),
        'region_cells': region_cells,
    }
    return problem, meta


# ── Public API ─────────────────────────────────────────────────────────────

def generate_problems_grid(path_drive_csv_in: str,
                           path_drive_grids_pkl: str,
                           path_drive_pkl_out: str,
                           path_drive_csv_out: str,
                           seed: int | None = None,
                           ) -> None:
    """
    ============================================================================
     Read the s_2 skeleton from `path_drive_csv_in`, load grids from
     `path_drive_grids_pkl`, and cross-join each skeleton row with the
     max_steps axis to build the (min_dist x max_steps) problem grid
     (k = `_K` goals per instance). Upload the detached problem list as a
     pickle to `path_drive_pkl_out` and per-instance metadata as a CSV to
     `path_drive_csv_out` (one row per built instance).

     Iteration is stable -- sorted by (domain, map), then skeleton order
     (ascending min_dist), then ascending max_steps -- so the single
     seeded RNG yields reproducible goal draws across re-runs. Instances
     whose rebuilt region holds fewer than `_K` cells are skipped (coverage
     visible in the log and as missing CSV rows). Skeleton maps absent
     from the grids bundle are skipped with a warning.
    ============================================================================
    """
    _log.info(f'generate_problems_grid('
              f'in={path_drive_csv_in}, '
              f'grids_pkl={path_drive_grids_pkl}, '
              f'pkl_out={path_drive_pkl_out}, '
              f'csv_out={path_drive_csv_out}, '
              f'k={_K}, max_steps={_MAX_STEPS})')
    drive = Drive.Factory.valdas()
    groups = _read_skeleton_grouped(drive=drive,
                                    path_drive_csv=path_drive_csv_in)
    grids_by_name = _load_grids_by_name(drive=drive,
                                        path_drive_pkl=path_drive_grids_pkl)
    rng = random.Random(seed)
    problems: list[ProblemGrid] = []
    rows: list[dict] = []
    # Stable iteration order -- required for seed-stable RNG draws.
    for (domain, name), skeleton in sorted(groups.items()):
        grid = grids_by_name.get(name)
        if grid is None:
            _log.warning(f'  skipping {name}: not in grids pickle '
                         f'({len(skeleton):,} skeleton rows dropped)')
            continue
        _log.info(f'  building <= {len(skeleton) * len(_MAX_STEPS):,} '
                  f'instances on {name} '
                  f'({len(skeleton)} bands x {len(_MAX_STEPS)} radii)')
        built = 0
        for rec in skeleton:
            for max_steps in _MAX_STEPS:
                result = _build_instance(grid=grid,
                                         rec=rec,
                                         max_steps=max_steps,
                                         rng=rng)
                if result is None:
                    continue
                problem, meta = result
                rows.append(meta)
                problem.detach()
                problems.append(problem)
                built += 1
        _log.info(f'    done: {built:,} instances on {name}')
    drive.upload_pickle(obj=problems, path=path_drive_pkl_out)
    _log.info(f'uploaded pkl -> {path_drive_pkl_out} '
              f'({len(problems):,} problems)')
    drive.upload_rows(rows=rows,
                      columns=_CSV_COLUMNS,
                      path=path_drive_csv_out)
    _log.info(f'uploaded csv -> {path_drive_csv_out}')


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters -- goal_distance step s_3: cross-join the s_2 skeleton
    # with max_steps to emit the 5x5 phase-diagram problem grid per map.
    # k=200 fixed; seed=0 for reproducible goal draws.
    path_drive_csv_in = (
        'Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv')
    path_drive_grids_pkl = 'Experiments/Grids/grids.pkl'
    path_drive_pkl_out = (
        'Experiments/OMSPP/goal_distance/i_3_problems_grid.pkl')
    path_drive_csv_out = (
        'Experiments/OMSPP/goal_distance/i_3_problems_grid.csv')
    seed = 0
    # Run
    generate_problems_grid(path_drive_csv_in=path_drive_csv_in,
                           path_drive_grids_pkl=path_drive_grids_pkl,
                           path_drive_pkl_out=path_drive_pkl_out,
                           path_drive_csv_out=path_drive_csv_out,
                           seed=seed)
    _log.info('--- done ---')
