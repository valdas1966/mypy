"""
===============================================================================
 Script: run kA*-INC in **extended mode** across the 25 nested-k goal
 families from `s_3_problems`, parallelized over a process pool, and
 emit cumulative counters per k-checkpoint to a single CSV on Drive.

 For each of the 25 (domain, map) pairs, the chain is:

   run([g_1..g_10])  ->  extend([g_11..g_20])  ->  ...  ->  extend([g_191..g_200])

 Snapshots are taken at every k in [10, 20, ..., 200] -- one CSV row
 per snapshot per chain (25 * 20 = 500 rows).
-------------------------------------------------------------------------------
 Parallelism
   Built on `ProblemGrid.Runner` (ProcessPoolExecutor):
     - 10 workers (default).
     - Each worker loads `Experiments/Grids/grids.pkl` exactly ONCE at
       init time; heavy GridMap objects stay in worker memory.
     - Each worker pre-builds one shared `StateCell` cache per grid,
       so all chains executed on that worker reuse the same cache.
     - Per-task IPC payload = light detached `ProblemGrid` only.

 Work unit -- 25 tasks, not 500
   The 500 problems are 25 nested-k chains x 20 k-checkpoints. Extended
   mode requires ONE kA*-INC run per chain with 20 snapshots. So we
   filter the 500-problem pickle down to the 25 `k=200` problems (each
   carries the full 200-goal sequence) and submit those to the Runner.
   The worker derives the k=10..190 prefixes internally by slicing
   `problem._goals` -- the same technique used by `_tester_extend.py`.

 Output CSV columns (15 cols, all CUMULATIVE since `run()`)
   domain, map, k,
   cnt_h_search, cnt_h_update, cnt_push, cnt_pop, cnt_decrease,
   cnt_expanded, cnt_generated, mem_open, mem_closed,
   elapsed_total, elapsed_search, elapsed_update

   No `mem_aux` column (2026-05-23 merge): KAStarAgg now folds
   its aux peak into `mem_open` (free-on-close + region
   attribution), so the cross-algo schema is just
   `mem_open` / `mem_closed` for every algo.

 Per-stage incremental deltas are a trivial post-processing step:
   df.groupby(['domain', 'map']).diff()
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle

 Output  (Drive)
   Experiments/OMSPP/kastar_inc_extended.csv

 Toy mode
   `n_problems` (None = all 500) slices the 500-problem pickle to the
   first N entries BEFORE the k=200 filter. Since problems are stored
   as 25 chains x 20 k-values consecutively, `n_problems=50` yields
   2 complete chains (k=200 sits at indices 19 and 39), so 40 CSV
   rows. `n_problems < 20` strips all k=200 problems and raises.
   When in toy mode, the output CSV gets a `_toy{N}` suffix to avoid
   clobbering full-run results.
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

# k-checkpoints -- matches s_3_problems.py: range(10, 201, 10).
_KS = list(range(10, 201, 10))

# Final k -- chains carry their full goal sequence at this length.
_K_FINAL = _KS[-1]


# ── Heuristic (module-level so it's picklable for spawn workers) ────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid -- bi-arg form expected by
     KAStarInc (each sub-search closes over its goal via default-arg
     idiom inside the algo).
    ============================================================================
    """
    return float(s.distance(g))


# ── Snapshot helper ─────────────────────────────────────────────────────────

def _snapshot(domain: str,
              map_name: str,
              k: int,
              algo: KAStarInc) -> dict:
    """
    ========================================================================
     Build one CSV row from the algo's cumulative counters and
     elapsed buckets at the current k-checkpoint.
    ========================================================================
    """
    c = algo.counters
    return {
        'domain':         domain,
        'map':            map_name,
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


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ──

def _experiment_kastar_inc_extended(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run one extend chain on `problem` (expected to carry 200 goals).
     Returns 20 CSV rows (one per k-checkpoint), cumulative counters.

     The `problem` arrives attached to its grid (Runner does this in
     `_worker_task`). We slice `_goals` to the first 10 goals, build
     KAStarInc, `run()` once, then loop 19 times calling `extend()` on
     the next 10 goals, snapshotting after each stage.
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    goals_all = list(problem._goals)
    if len(goals_all) != _K_FINAL:
        raise ValueError(
            f'expected {_K_FINAL} goals, got {len(goals_all)} on '
            f'{domain}/{map_name}')

    _log.info(f'start  ({domain}, {map_name}) k=10..{_K_FINAL}')

    # Stage 1: solve k=10 from scratch.
    problem._goals = goals_all[:_KS[0]]
    algo = KAStarInc(problem=problem, h=_h)
    algo.run()
    rows = [_snapshot(domain=domain, map_name=map_name,
                      k=_KS[0], algo=algo)]

    # Stages 2..20: extend by 10 goals each.
    for k_target in _KS[1:]:
        new_goals = goals_all[k_target - 10:k_target]
        algo.extend(new_goals)
        rows.append(_snapshot(domain=domain, map_name=map_name,
                              k=k_target, algo=algo))

    last = rows[-1]
    _log.info(f'done   ({domain}, {map_name}) '
              f'elapsed={last["elapsed_total"]:.2f}s '
              f'expanded@k{_K_FINAL}={last["cnt_expanded"]:,}')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_extended_benchmark(path_drive_pkl_in: str,
                           path_drive_grids_in: str,
                           path_drive_csv_out: str,
                           workers: int = 10,
                           n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-INC in extended mode across the nested-k chains found in
     `path_drive_pkl_in`, parallelized over `workers` worker processes.
     Emit one CSV at `path_drive_csv_out` on Drive.

     `n_problems` slices the loaded problem list to the first N entries
     BEFORE the k=200 filter. None (default) processes all 500
     problems -> 25 chains -> 500 CSV rows. Toy example: N=50 ->
     2 chains -> 40 rows. N<20 -> 0 chains -> ValueError.

     `workers` is auto-clamped to `min(workers, n_chains)` -- no point
     spawning idle worker processes that each hold the grids in RAM.

     Flow
       1. Download the detached-problems pickle and grids pickle to
          `/tmp/`.
       2. Load via `ProblemGrid.Store.load` (binds shared StateCell
          cache per grid).
       3. Optionally slice to `n_problems` for toy mode.
       4. Filter to k=200 problems (one per (domain, map) pair).
       5. Re-pickle the filtered subset (light; up to 25 problems).
       6. Run `ProblemGrid.Runner.run` with the experiment callable.
       7. Flatten the chain results into CSV rows; write; upload.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'kastar_inc_extended: workers={workers}')

    # Allocate temp files up front so the finally block can clean them
    # unconditionally.
    fd_in, path_in = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_in)
    fd_g, path_grids = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_g)
    fd_filt, path_filt = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_filt)
    fd_csv, path_csv = tempfile.mkstemp(suffix='.csv')
    os.close(fd_csv)

    try:
        # 1. Download.
        _log.info(f'downloading {path_drive_pkl_in}')
        drive.download(path_src=path_drive_pkl_in, path_dest=path_in)
        _log.info(f'downloading {path_drive_grids_in}')
        drive.download(path_src=path_drive_grids_in, path_dest=path_grids)

        # 2. Load (auto-binds).
        problems, grids = ProblemGrid.Store.load(
            path_problems=path_in,
            path_grids=path_grids)
        _log.info(f'loaded: {len(problems):,} problems, '
                  f'{len(grids):,} grids')

        # 3. Optional toy-mode slice (pre-filter).
        if n_problems is not None:
            if n_problems < 1:
                raise ValueError(
                    f'n_problems must be >= 1; got {n_problems}')
            problems = problems[:n_problems]
            _log.info(f'toy mode: sliced to first '
                      f'{len(problems):,} problems')

        # 4. Filter to k=200 chains.
        filtered = [p for p in problems
                    if len(p.goals_rc) == _K_FINAL]
        if not filtered:
            raise ValueError(
                f'no k={_K_FINAL} problems in the sliced set '
                f'(n_problems={n_problems!r}). Use n_problems >= 20 '
                f'so at least one k={_K_FINAL} problem is included.')
        n_chains = len(filtered)
        _log.info(f'filtered: {n_chains:,} k={_K_FINAL} chains '
                  f'(one per (domain, map) pair)')

        # 5. Re-pickle the filtered subset. __getstate__ drops grid +
        # state cache automatically, so the file stays light.
        with open(path_filt, 'wb') as f:
            pickle.dump(filtered, f, protocol=pickle.HIGHEST_PROTOCOL)

        # 6. Run on the pool. Each worker loads `path_grids` once, builds
        # a shared per-grid StateCell cache, then processes its share of
        # the chains. Clamp workers to chain count -- otherwise idle
        # workers each hold the (heavy) grids in RAM for no benefit.
        effective_workers = min(workers, n_chains)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_chains={n_chains}); '
                  f'dispatching {n_chains:,} chains '
                  f'(each = {len(_KS):,} snapshots; chunksize=1)')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_kastar_inc_extended,
            workers=effective_workers,
            chunksize=1)

        # 7. Flatten + write CSV + upload.
        rows = [row for chain_rows in results for row in chain_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} chains x {len(_KS):,} k-stages); '
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
    # The __main__ guard is mandatory: macOS uses `spawn` for
    # ProcessPoolExecutor, so each worker re-imports this module.
    # Without the guard, every worker would re-launch the benchmark.
    #
    # ── Mode toggle ─────────────────────────────────────────────────
    # IS_EXTRA=False -> read canonical i_3_problems.pkl; write
    #                   kastar_inc_extended.csv.
    # IS_EXTRA=True  -> read i_3_problems_extra.pkl (build via s_3
    #                   with IS_EXTRA=True first); write
    #                   kastar_inc_extended_extra.csv.
    IS_EXTRA = False
    extra_suffix = '_extra' if IS_EXTRA else ''

    path_drive_pkl_in = (f'Experiments/OMSPP/'
                         f'i_3_problems{extra_suffix}.pkl')
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: process only the first N problems of the pickle (None
    # == all). Slicing happens BEFORE the k=200 filter, so the chain
    # count is roughly N // 20. Useful for smoke-testing.
    n_problems = None    # full run: set to None

    # Output path -- combine the extras suffix with any toy-mode
    # suffix; toy never clobbers the full-run CSV.
    toy_suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/OMSPP/'
                          f'kastar_inc_extended'
                          f'{extra_suffix}{toy_suffix}.csv')

    run_extended_benchmark(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
