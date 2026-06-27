"""
===============================================================================
 goal_distance step s_5 -- run kA*-AGG (Φ=MIN, opt+sv) in both eager and
 lazy modes across the (min_dist x max_steps) phase-diagram grid from s_3,
 parallelized over a process pool. 2 configs per problem; one CSV row per
 (problem, config) on Drive.

 Mirrors the parent OMSPP s_5 verbatim except: k is FIXED at 200 (geometry
 is the swept axis, not k), and each row is tagged with the (min_dist,
 max_steps) phase-diagram coordinates recovered from the problem name
 (`{map}_d{min_dist:03d}_s{max_steps:02d}`, set in s_3).

 Why these 2 configs
   The (is_opt=True, store_vector=True) pair on eager and lazy -- the
   canonical INC-vs-AGG comparison set. is_opt=True requires agg in
   {MIN, MAX}; we use MIN.

 Why NOT extended mode
   KAStarAgg is not Extendable, so every problem is solved from scratch
   per config (which is exactly what we want at fixed k=200).
-------------------------------------------------------------------------------
 Parallelism (ProblemGrid.Runner / ProcessPoolExecutor)
   - workers default 10, auto-clamped to min(workers, n_problems).
   - each worker loads grids.pkl once; one shared StateCell cache per grid.
   - per-task IPC payload = light detached ProblemGrid only.

 Output CSV columns (22)
   IDs (5):        domain, map, min_dist, max_steps, k
   Config (4):     is_lazy, is_opt, store_vector, config
   Counters (11):  cnt_h_search, cnt_h_update,
                   cnt_phi_search, cnt_phi_update,
                   cnt_push, cnt_pop, cnt_decrease,
                   cnt_expanded, cnt_generated,
                   mem_open, mem_closed
                   (mem_open folds the AGG aux peak)
   Timing (3):     elapsed_total, elapsed_search, elapsed_update

   cnt_*_update / elapsed_update are 0 for lazy configs by design.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/goal_distance/i_3_problems_grid.pkl
   Experiments/Grids/grids.pkl
 Output  (Drive)
   Experiments/OMSPP/goal_distance/kastar_agg_grid.csv

 Toy mode
   `n_problems` (None = all) slices the pickle to the first N problems;
   the output CSV gets a `_toy{N}` suffix so it never clobbers the
   full-run result.
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
from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Φ aggregation. is_opt requires MIN or MAX; we pick MIN.
_AGG = 'MIN'


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'min_dist',
    'max_steps',
    'k',
    'is_lazy',
    'is_opt',
    'store_vector',
    'config',
    'cnt_h_search',
    'cnt_h_update',
    'cnt_phi_search',
    'cnt_phi_update',
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


# (is_lazy, is_opt, store_vector) -- the 2 canonical comparison configs.
_CONFIGS: list[tuple[bool, bool, bool]] = [
    (False, True, True),   # eager_opt_sv
    (True,  True, True),   # lazy_opt_sv
]


# ── Heuristic (module-level so it's picklable for spawn workers) ────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid -- bi-arg form expected by
     KAStarAgg (each sub-search closes over its goal via default-arg
     idiom inside the algo).
    ============================================================================
    """
    return float(s.key.distance(g.key))


def _config_name(is_lazy: bool,
                 is_opt: bool,
                 store_vector: bool) -> str:
    """
    ============================================================================
     Build a folder-safe config name like 'lazy_opt_sv' (matches the
     parent OMSPP s_5 / _dump_csvs labels so artifacts align).
    ============================================================================
    """
    lazy = 'lazy' if is_lazy else 'eager'
    opt = 'opt' if is_opt else 'noopt'
    sv = 'sv' if store_vector else 'nosv'
    return f'{lazy}_{opt}_{sv}'


def _parse_coords(name: str) -> tuple[int, int]:
    """
    ============================================================================
     Recover (min_dist, max_steps) from a problem name shaped
     '{map}_d{min_dist:03d}_s{max_steps:02d}' (set in s_3). rsplit from the
     right is robust to underscores inside the map name.
    ============================================================================
    """
    base, s_part = name.rsplit('_s', 1)
    _, d_part = base.rsplit('_d', 1)
    return int(d_part), int(s_part)


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ──

def _experiment_kastar_agg_grid(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run the 2 (eager_opt_sv, lazy_opt_sv) kA*-AGG configs (Φ=`_AGG`) on
     `problem` and return 2 CSV rows, each tagged with the (min_dist,
     max_steps) phase-diagram coordinates.

     The `problem` arrives attached to its grid (Runner does this).
     KAStarAgg reads `problem.goals` once and never mutates it, so a fresh
     instance per config on the same problem object is safe.
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    min_dist, max_steps = _parse_coords(name=problem.name)
    k = len(problem.goals_rc)

    _log.info(f'start  ({domain}, {map_name}, '
              f'd={min_dist}, s={max_steps}, k={k}) '
              f'{len(_CONFIGS)} configs')

    rows: list[dict] = []
    for is_lazy, is_opt, store_vector in _CONFIGS:
        cfg = _config_name(is_lazy=is_lazy,
                           is_opt=is_opt,
                           store_vector=store_vector)
        algo = KAStarAgg(problem=problem,
                         h=_h,
                         agg=_AGG,
                         is_lazy=is_lazy,
                         is_opt=is_opt,
                         store_vector=store_vector)
        algo.run()
        c = algo.counters
        rows.append({
            'domain':         domain,
            'map':            map_name,
            'min_dist':       min_dist,
            'max_steps':      max_steps,
            'k':              k,
            'is_lazy':        is_lazy,
            'is_opt':         is_opt,
            'store_vector':   store_vector,
            'config':         cfg,
            'cnt_h_search':   c['cnt_h_search'],
            'cnt_h_update':   c['cnt_h_update'],
            'cnt_phi_search': c['cnt_phi_search'],
            'cnt_phi_update': c['cnt_phi_update'],
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
        })

    total_elapsed = sum(r['elapsed_total'] for r in rows)
    _log.info(f'done   ({domain}, {map_name}, '
              f'd={min_dist}, s={max_steps}) '
              f'{len(_CONFIGS)} configs in {total_elapsed:.2f}s')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_agg_grid(path_drive_pkl_in: str,
                 path_drive_grids_in: str,
                 path_drive_csv_out: str,
                 workers: int = 10,
                 n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-AGG (Φ=`_AGG`, 2 configs) across every problem in
     `path_drive_pkl_in`, parallelized over `workers` worker processes,
     and emit one CSV at `path_drive_csv_out` on Drive (2 rows / problem).

     `n_problems` slices the loaded problem list to the first N entries
     (toy mode); None processes all. `workers` is auto-clamped to
     min(workers, n_problems).
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'kastar_agg_grid: agg={_AGG}, workers={workers}, '
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
                  f'each task = 1 problem x {len(_CONFIGS):,} configs '
                  f'-> {n_tasks * len(_CONFIGS):,} kA*-AGG runs total')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_kastar_agg_grid,
            workers=effective_workers,
            chunksize=1)

        rows = [row for task_rows in results for row in task_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} tasks x {len(_CONFIGS):,} configs); '
                  f'writing CSV')
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
        f'kastar_agg_grid{toy_suffix}.csv')

    run_agg_grid(path_drive_pkl_in=path_drive_pkl_in,
                 path_drive_grids_in=path_drive_grids_in,
                 path_drive_csv_out=path_drive_csv_out,
                 workers=workers,
                 n_problems=n_problems)
    _log.info('--- done ---')
