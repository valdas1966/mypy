"""
===============================================================================
 goal_distance step s_4 -- run kA*-INC once per problem across the
 (min_dist x max_steps) phase-diagram grid from s_3, parallelized over a
 process pool, and emit one CSV row per problem on Drive.

 k is FIXED at 200 here (the grid axes are geometry, not k), so -- unlike
 the parent OMSPP s_4 -- there is NO extend chain: each problem is solved
 from scratch with a single run(). One Runner task = one problem = one row.

 The (min_dist, max_steps) coordinates are recovered from the problem name
 (`{map}_d{min_dist:03d}_s{max_steps:02d}`, set in s_3) -- the name
 survives detach / pickle.
-------------------------------------------------------------------------------
 Parallelism (ProblemGrid.Runner / ProcessPoolExecutor)
   - workers default 10, auto-clamped to min(workers, n_problems).
   - each worker loads grids.pkl once; one shared StateCell cache per grid.
   - per-task IPC payload = light detached ProblemGrid only.

 Output CSV columns (14, all CUMULATIVE for the single run)
   domain, map, min_dist, max_steps, k,
   cnt_h_search, cnt_h_update, cnt_push, cnt_pop, cnt_decrease,
   cnt_expanded, cnt_generated, mem_open, mem_closed,
   elapsed_total, elapsed_search, elapsed_update
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/goal_distance/i_3_problems_grid.pkl
   Experiments/Grids/grids.pkl
 Output  (Drive)
   Experiments/OMSPP/goal_distance/kastar_inc_grid.csv

 Toy mode
   `n_problems` (None = all) slices the problem pickle to the first N
   entries; the output CSV gets a `_toy{N}` suffix so it never clobbers
   the full-run result.
===============================================================================
"""
import os
import csv
import pickle
import tempfile
import logging

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'min_dist',
    'rep',
    'max_steps',
    'k',
    'cnt_h_search',
    'cnt_h_update',
    'cnt_push',
    'cnt_pop',
    'cnt_decrease',
    'cnt_expanded',
    'cnt_generated',
    'mem_open',
    'mem_closed',
    'elapsed_total',
    'elapsed_search',
    'elapsed_update',
]


# ── Heuristic (module-level so it's picklable for spawn workers) ────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid -- bi-arg form expected by
     KAStarInc (each sub-search closes over its goal via default-arg
     idiom inside the algo).
    ============================================================================
    """
    return float(s.key.distance(g.key))


def _parse_coords(name: str) -> tuple[int, int, int]:
    """
    ============================================================================
     Recover (min_dist, max_steps, rep) from a problem name shaped
     '{map}_d{min_dist:03d}_r{rep:02d}_s{max_steps:02d}' (set in s_3).
     rsplit from the right is robust to underscores inside the map name.
    ============================================================================
    """
    base, s_part = name.rsplit('_s', 1)
    base, r_part = base.rsplit('_r', 1)
    _, d_part = base.rsplit('_d', 1)
    return int(d_part), int(s_part), int(r_part)


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ──

def _experiment_kastar_inc_grid(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run kA*-INC once on `problem` (k=200, single run() -- no extend) and
     return one CSV row of cumulative counters + elapsed buckets, tagged
     with the (min_dist, max_steps) phase-diagram coordinates.

     The `problem` arrives attached to its grid (Runner does this).
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    min_dist, max_steps, rep = _parse_coords(name=problem.name)
    k = len(problem.goals_rc)

    _log.info(f'start  ({domain}, {map_name}, '
              f'min_dist={min_dist}, max_steps={max_steps}, '
              f'rep={rep}, k={k})')

    algo = KAStarInc(problem=problem, h=_h)
    algo.run()
    c = algo.counters
    row = {
        'domain':         domain,
        'map':            map_name,
        'min_dist':       min_dist,
        'rep':            rep,
        'max_steps':      max_steps,
        'k':              k,
        'cnt_h_search':   c['cnt_h_search'],
        'cnt_h_update':   c['cnt_h_update'],
        'cnt_push':       c['cnt_push'],
        'cnt_pop':        c['cnt_pop'],
        'cnt_decrease':   c['cnt_decrease'],
        'cnt_expanded':   c['cnt_expanded'],
        'cnt_generated':  c['cnt_generated'],
        'mem_open':       c['mem_open'],
        'mem_closed':     c['mem_closed'],
        'elapsed_total':  round(algo.elapsed, 6),
        'elapsed_search': round(algo.elapsed_search, 6),
        'elapsed_update': round(algo.elapsed_update, 6),
    }
    _log.info(f'done   ({domain}, {map_name}, '
              f'd={min_dist}, s={max_steps}) '
              f'elapsed={row["elapsed_total"]:.2f}s '
              f'expanded={row["cnt_expanded"]:,}')
    return [row]


# ── Public API ─────────────────────────────────────────────────────────────

def run_inc_grid(path_drive_pkl_in: str,
                 path_drive_grids_in: str,
                 path_drive_csv_out: str,
                 workers: int = 10,
                 n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-INC across every problem in `path_drive_pkl_in` (one run per
     problem), parallelized over `workers` worker processes, and emit one
     CSV at `path_drive_csv_out` on Drive (one row per problem).

     `n_problems` slices the loaded problem list to the first N entries
     (toy mode); None processes all. `workers` is auto-clamped to
     min(workers, n_problems).
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'kastar_inc_grid: workers={workers}, '
              f'n_problems={n_problems}')

    fd_in, path_in = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_in)
    fd_g, path_grids = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_g)
    fd_filt, path_filt = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_filt)
    fd_csv, path_csv = tempfile.mkstemp(suffix='.csv')
    os.close(fd_csv)

    try:
        _log.info(f'downloading {path_drive_pkl_in}')
        drive.download(path_src=path_drive_pkl_in, path_dest=path_in)
        _log.info(f'downloading {path_drive_grids_in}')
        drive.download(path_src=path_drive_grids_in, path_dest=path_grids)

        problems, grids = ProblemGrid.Store.load(
            path_problems=path_in,
            path_grids=path_grids)
        _log.info(f'loaded: {len(problems):,} problems, '
                  f'{len(grids):,} grids')

        if n_problems is not None:
            if n_problems < 1:
                raise ValueError(
                    f'n_problems must be >= 1; got {n_problems}')
            problems = problems[:n_problems]
            _log.info(f'toy mode: sliced to first '
                      f'{len(problems):,} problems')

        n_tasks = len(problems)
        if n_tasks == 0:
            raise ValueError('no problems to run')

        with open(path_filt, 'wb') as f:
            pickle.dump(problems, f, protocol=pickle.HIGHEST_PROTOCOL)

        effective_workers = min(workers, n_tasks)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'one kA*-INC run per problem')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_kastar_inc_grid,
            workers=effective_workers,
            chunksize=1)

        rows = [row for task_rows in results for row in task_rows]
        _log.info(f'received {len(rows):,} rows; writing CSV')
        with open(path_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=_CSV_COLUMNS,
                                    extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        drive.upload(path_src=path_csv,
                     path_dest=path_drive_csv_out)
        _log.info(f'uploaded csv -> {path_drive_csv_out}')

    finally:
        for path in (path_in, path_grids, path_filt, path_csv):
            if os.path.exists(path):
                os.unlink(path)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # The __main__ guard is mandatory: spawn workers re-import this module.
    path_drive_pkl_in = (
        'Experiments/OMSPP/goal_distance/i_3_problems_grid.pkl')
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: process only the first N problems (None == all).
    n_problems = None

    toy_suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (
        f'Experiments/OMSPP/goal_distance/'
        f'kastar_inc_grid{toy_suffix}.csv')

    run_inc_grid(path_drive_pkl_in=path_drive_pkl_in,
                 path_drive_grids_in=path_drive_grids_in,
                 path_drive_csv_out=path_drive_csv_out,
                 workers=workers,
                 n_problems=n_problems)
    _log.info('--- done ---')
