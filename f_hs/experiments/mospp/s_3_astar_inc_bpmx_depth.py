"""
===============================================================================
 Script: run AStarIncMOSPP across the 500 OMSPP problems of
 `Experiments/OMSPP/i_3_problems.pkl`, each FLIPPED into a MOSPP
 instance, sweeping the in-search BPMX depth. Parallelized over a
 process pool; emits one CSV row per (problem, depth_bpmx) to Drive.

 Each OMSPP problem (1 start, k goals) is reused as a MOSPP problem
 (k starts, 1 goal) via `ProblemSPP.flipped()` -- a zero-copy
 start<->goal swap, exact on the undirected experiment grids.
-------------------------------------------------------------------------------
 Fixed algorithm config (the requested spec)
   algorithm    : AStarIncMOSPP    (only -- no AStarRepMOSPP baseline)
   carry_cache  : True       } "only cached" reuse mode -- the on-path
   carry_bounds : False      }  cache is the ONLY carried store
   propagate    : False      ("depth_prop=0" -- no pathmax propagation)
   rule_bpmx    : '1'
   depth_bpmx   : swept over [0, 1, 2, 3, 4, 5, None]. The algorithm
                  rejects a literal depth_bpmx=0 (BPMXMixin needs an
                  int >= 1 or None), so the 0 point is run with BPMX
                  fully OFF -- rule_bpmx=None -- as the no-BPMX
                  baseline, and is still labelled depth_bpmx=0 in the
                  CSV (with rule_bpmx=none). None == BPMX to
                  convergence.

 This is the oracle's Group-C ("only BPMX") config family -- see
 `f_hs/algo/i_1_mospp/i_1_astar_inc/study/oracle.py` -- with the
 depth sweep widened from {1,2,3,None} to {0,1,2,3,4,5,None}.
-------------------------------------------------------------------------------
 Work unit -- one task per problem
   Each task flips its problem once, then runs AStarIncMOSPP 7 times
   (one per depth_bpmx) on the one flipped view, returning 7 CSV
   rows. 500 problems x 7 depths = 3,500 rows.

 Parallelism
   Built on `ProblemGrid.Runner` (ProcessPoolExecutor):
     - `workers` worker processes (default 10).
     - Each worker loads `Experiments/Grids/grids.pkl` once at init;
       the heavy GridMap objects + a shared StateCell cache per grid
       stay in worker memory.
     - Per-task IPC payload = one light detached ProblemGrid + 7 rows.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle

 Output  (Drive)
   Experiments/MOSPP/astar_inc_bpmx_depth.csv

 Toy mode
   `n_problems` (None = all 500) slices the problem list to the first
   N entries -> N x 7 rows. The output CSV gets a `_toy{N}` suffix so
   a smoke run never clobbers the full-run CSV.

 Compute note
   A full run is 3,500 AStarIncMOSPP runs; each is m sequential A*
   sub-searches (m in [10..200]) -- on the order of 370k inner A*
   searches total. Heavy: give it cores and let it churn.
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
from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Fixed algorithm config ──────────────────────────────────────────────────
# "only cached": carry the on-path cache across sub-searches, nothing
# else. carry_bounds=False so the cache is the sole reuse store.
_CARRY_CACHE = True
_CARRY_BOUNDS = False
# "depth_prop=0": no pre-search pathmax propagation.
_PROPAGATE = False
# BPMX rule held fixed; depth is the swept axis. 0 == BPMX-off baseline
# (run as rule_bpmx=None, since the algorithm rejects a literal
# depth_bpmx=0); None == BPMX to convergence.
_RULE_BPMX = '1'
_DEPTHS_BPMX = [0, 1, 2, 3, 4, 5, None]


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain', 'map', 'm', 'rule_bpmx', 'depth_bpmx',
    'cnt_expanded', 'cnt_generated',
    'cnt_prop_attempts', 'cnt_prop_lifts', 'cnt_prop_waves',
    'cnt_bpmx_attempts', 'cnt_bpmx_lifts', 'cnt_bpmx_depth',
    'cnt_h_search',
    'cnt_push', 'cnt_pop', 'cnt_decrease',
    'cnt_cache_hits_at_init',
    'mem_open', 'mem_closed', 'mem_cache', 'mem_bounds', 'mem_total',
    'elapsed_total', 'elapsed_search', 'elapsed_update',
]

# Counter columns pulled straight from `algo.counters`.
_COUNTER_NAMES = [c for c in _CSV_COLUMNS
                  if c.startswith(('cnt_', 'mem_'))]


# ── Heuristic (module-level so it ships to spawn workers) ───────────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid StateCells -- bi-arg form
     `h(state, goal)` expected by AStarIncMOSPP.
    ============================================================================
    """
    return float(s.distance(g))


# ── Row builder ─────────────────────────────────────────────────────────────

def _row(domain: str,
         map_name: str,
         m: int,
         rule_bpmx,
         depth_bpmx,
         algo: AStarIncMOSPP) -> dict:
    """
    ============================================================================
     Build one CSV row from a finished AStarIncMOSPP run: its
     counters + elapsed buckets, tagged with the problem identity,
     the `rule_bpmx` actually used (None -> 'none', the BPMX-off
     baseline), and the swept `depth_bpmx` value (None -> 'inf').
    ============================================================================
    """
    c = dict(algo.counters.items())
    row = {
        'domain':         domain,
        'map':            map_name,
        'm':              m,
        'rule_bpmx':      'none' if rule_bpmx is None else rule_bpmx,
        'depth_bpmx':     'inf' if depth_bpmx is None else depth_bpmx,
        'elapsed_total':  round(algo.elapsed, 6),
        'elapsed_search': round(algo.elapsed_search, 6),
        'elapsed_update': round(algo.elapsed_update, 6),
    }
    for name in _COUNTER_NAMES:
        row[name] = c.get(name, 0)
    return row


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ───

def _experiment_bpmx_depth(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run the depth_bpmx sweep on one problem.

     `problem` arrives attached (the Runner does this). It is an
     OMSPP-shaped ProblemGrid (1 start, k goals); `flipped()` turns
     it into a MOSPP problem (k starts, 1 goal). AStarIncMOSPP is
     then run once per `depth_bpmx` in `_DEPTHS_BPMX`, all on the
     one flipped view.

     Returns one row dict per depth -- 7 rows.
    ============================================================================
    """
    domain = getattr(problem.grid, 'domain', '') or ''
    map_name = problem.grid_name
    # The OMSPP goal count becomes the MOSPP start count after flip.
    m = len(problem.goals_rc)
    mospp = problem.flipped()
    _log.info(f'start  ({domain}, {map_name}) m={m}')
    rows: list[dict] = []
    for depth in _DEPTHS_BPMX:
        # depth 0 is the BPMX-OFF baseline: the algorithm rejects a
        # literal depth_bpmx=0 (BPMXMixin needs >=1 or None), so run
        # it with BPMX fully disabled (rule_bpmx=None). The row is
        # still labelled depth_bpmx=0.
        if depth == 0:
            rule_bpmx, depth_arg = None, None
        else:
            rule_bpmx, depth_arg = _RULE_BPMX, depth
        algo = AStarIncMOSPP(
            problem=mospp,
            h=_h,
            is_recording=False,
            is_timing=True,
            carry_cache=_CARRY_CACHE,
            carry_bounds=_CARRY_BOUNDS,
            propagate=_PROPAGATE,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_arg,
        )
        algo.run()
        rows.append(_row(domain=domain, map_name=map_name, m=m,
                         rule_bpmx=rule_bpmx, depth_bpmx=depth,
                         algo=algo))
    last = rows[-1]
    _log.info(f'done   ({domain}, {map_name}) m={m} '
              f'elapsed@last={last["elapsed_total"]:.2f}s')
    return rows


# ── Public API ──────────────────────────────────────────────────────────────

def run_bpmx_depth_sweep(path_drive_pkl_in: str,
                         path_drive_grids_in: str,
                         path_drive_csv_out: str,
                         workers: int = 10,
                         n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run AStarIncMOSPP across every problem in `path_drive_pkl_in`
     (OMSPP problems, flipped to MOSPP), sweeping `depth_bpmx` over
     `_DEPTHS_BPMX`. Parallelized over `workers` processes. Emits one
     CSV to `path_drive_csv_out` on Drive -- one row per
     (problem, depth_bpmx).

     `n_problems` slices the loaded problem list to the first N
     entries (toy / smoke mode); None processes all of them.
     `workers` is clamped to `min(workers, n_tasks)`.

     Flow:
       1. Download the OMSPP problems pickle + grids pickle to /tmp.
       2. Optionally slice to `n_problems`; re-pickle for the Runner.
       3. `ProblemGrid.Runner.run` dispatches one task per problem;
          each worker attaches the problem, flips it, runs the
          7-depth sweep.
       4. Flatten the per-problem row lists; write + upload the CSV.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'astar_inc_bpmx_depth: workers={workers}, '
              f'rule_bpmx={_RULE_BPMX!r}, depths={_DEPTHS_BPMX}')

    # Allocate temp files up front so the finally block always cleans.
    fd_in, path_in = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_in)
    fd_g, path_grids = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_g)
    fd_run, path_run = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_run)
    fd_csv, path_csv = tempfile.mkstemp(suffix='.csv')
    os.close(fd_csv)

    try:
        # 1. Download inputs.
        _log.info(f'downloading {path_drive_pkl_in}')
        drive.download(path_src=path_drive_pkl_in, path_dest=path_in)
        _log.info(f'downloading {path_drive_grids_in}')
        drive.download(path_src=path_drive_grids_in,
                       path_dest=path_grids)

        # 2. Load, optional toy-slice, re-pickle for the Runner.
        with open(path_in, 'rb') as f:
            problems = pickle.load(f)
        _log.info(f'loaded {len(problems):,} problems')
        if n_problems is not None:
            if n_problems < 1:
                raise ValueError(
                    f'n_problems must be >= 1; got {n_problems}')
            problems = problems[:n_problems]
            _log.info(f'toy mode: sliced to first '
                      f'{len(problems):,} problems')
        with open(path_run, 'wb') as f:
            pickle.dump(problems, f,
                        protocol=pickle.HIGHEST_PROTOCOL)

        # 3. Dispatch one task per problem over the worker pool.
        n_tasks = len(problems)
        effective_workers = max(1, min(workers, n_tasks))
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'{n_tasks:,} tasks x {len(_DEPTHS_BPMX)} depths = '
                  f'{n_tasks * len(_DEPTHS_BPMX):,} runs '
                  f'(chunksize=1)')
        results = ProblemGrid.Runner.run(
            path_problems=path_run,
            path_grids=path_grids,
            experiment=_experiment_bpmx_depth,
            workers=effective_workers,
            chunksize=1)

        # 4. Flatten + write CSV + upload.
        rows = [r for prob_rows in results for r in prob_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} problems x '
                  f'{len(_DEPTHS_BPMX)} depths); writing CSV')
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
        for path in (path_in, path_grids, path_run, path_csv):
            if os.path.exists(path):
                os.unlink(path)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # The __main__ guard is mandatory: macOS uses `spawn` for
    # ProcessPoolExecutor, so each worker re-imports this module.
    # Without the guard, every worker would re-launch the sweep.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: process only the first N of the 500 problems
    # (None == all 500). Useful for smoke-testing before a full run.
    n_problems = None

    # Output path -- auto-suffix in toy mode so a smoke run never
    # clobbers the full-run CSV.
    suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/MOSPP/'
                          f'astar_inc_bpmx_depth{suffix}.csv')

    run_bpmx_depth_sweep(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
