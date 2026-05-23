"""
===============================================================================
 Script: run kA*-AGG with `is_opt=True, store_vector=True` on each
 mode (eager and lazy), aggregator Φ = MIN, across every problem in
 `s_3_problems.pkl`. 2 configs per problem (NOT the full 8-way sweep).
 Parallelized over a process pool; emits cumulative counters + timing
 per (problem, config) to a single CSV on Drive.

 Why only 2 configs (2026-05-15)
   Restricted from the 2x2x2 (=8) sweep to just the (opt=True,
   sv=True) pair on eager and lazy. The 2026-05-14 toy sweep showed
   sv=True ADDS ~15% elapsed on grid+Manhattan (h-vector upkeep
   exceeds h-recompute savings); the no-opt and no-sv baselines were
   captured in `kastar_agg_all_configs_toy50.csv` (still on Drive)
   and don't need to be re-measured for the full run. `is_opt=True`
   requires agg in {MIN, MAX}; we use MIN here.

 Why NOT extended mode
   KAStarAgg is NOT Extendable -- the single-loop Φ structure doesn't
   fit the per-goal extend model (per the algo matrix). So we run
   each of the 500 problems from scratch per config: 500 x 2 = 1000
   independent kA*-AGG runs.

 Work unit -- per problem, both configs
   Each Runner task processes one ProblemGrid and runs the 2 configs
   on it back-to-back (same problem object, same grid in worker RAM
   -> good cache locality). The task returns 2 CSV rows. Toy slice
   `n_problems=N` -> N tasks -> N*2 CSV rows.
-------------------------------------------------------------------------------
 Parallelism
   Built on `ProblemGrid.Runner` (ProcessPoolExecutor):
     - 10 workers (default), auto-clamped to `min(workers, n_tasks)`.
     - Each worker loads `Experiments/Grids/grids.pkl` exactly ONCE at
       init time; heavy GridMap objects stay in worker memory.
     - Each worker pre-builds one shared `StateCell` cache per grid.
     - Per-task IPC payload = light detached `ProblemGrid` only.

 Output CSV columns (21 cols)
   IDs (3):        domain, map, k
   Config (4):     is_lazy, is_opt, store_vector, config
   Counters (11):  cnt_h_search, cnt_h_update,
                   cnt_phi_search, cnt_phi_update,
                   cnt_push, cnt_pop, cnt_decrease,
                   cnt_expanded, cnt_generated,
                   mem_open, mem_closed
                   (`mem_open` folds the AGG aux peak ---
                    see `KAStarAgg._sync_memory_snapshot`)
   Timing (3):     elapsed_total, elapsed_search, elapsed_update

   `config` is the folder-safe label `{lazy|eager}_{opt|noopt}_{sv|nosv}`
   that matches the trace-CSV folder naming in `_dump_csvs.py`.

   `cnt_*_update` and `elapsed_update` are always 0 for lazy configs
   by design (lazy mode has no PHASE_UPDATE).
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle

 Output  (Drive)
   Experiments/OMSPP/kastar_agg_all_configs.csv

 Toy mode
   `n_problems` (None = all 500) slices the 500-problem pickle to the
   first N entries directly (no k-filter -- AGG runs all k values).
   N=50 -> 50 problems x 2 configs = 100 CSV rows. The output CSV
   gets a `_toy{N}` suffix in toy mode to avoid clobbering full-run
   results.
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


# Restricted sweep (2026-05-15): only the (opt=True, sv=True) pair
# for each mode -- 2 configs, not 8. The remaining 6 (any is_opt=False
# or any store_vector=False combination) are no longer measured here;
# the 2026-05-14 toy CSV remains on Drive as the historical 8-config
# snapshot. Sweep both modes so the lazy-vs-eager axis stays visible.
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
    return float(s.distance(g))


# ── Config-name helper (matches _dump_csvs._config_name) ────────────────────

def _config_name(is_lazy: bool,
                 is_opt: bool,
                 store_vector: bool) -> str:
    """
    ========================================================================
     Build a folder-safe config name like 'lazy_noopt_nosv'. Matches
     `_dump_csvs.py` so trace CSVs and benchmark rows align by label.
    ========================================================================
    """
    lazy = 'lazy' if is_lazy else 'eager'
    opt = 'opt' if is_opt else 'noopt'
    sv = 'sv' if store_vector else 'nosv'
    return f'{lazy}_{opt}_{sv}'


# ── Snapshot helper ─────────────────────────────────────────────────────────

def _snapshot(domain: str,
              map_name: str,
              k: int,
              is_lazy: bool,
              is_opt: bool,
              store_vector: bool,
              config: str,
              algo: KAStarAgg) -> dict:
    """
    ========================================================================
     Build one CSV row from the algo's counters and elapsed buckets
     after a single kA*-AGG run.
    ========================================================================
    """
    c = algo.counters
    return {
        'domain':         domain,
        'map':            map_name,
        'k':              k,
        'is_lazy':        is_lazy,
        'is_opt':         is_opt,
        'store_vector':   store_vector,
        'config':         config,
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
    }


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ──

def _experiment_kastar_agg_all_configs(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run the 2 (eager_opt_sv, lazy_opt_sv) configurations of
     kA*-AGG with Φ=`_AGG` on `problem`. Returns 2 CSV rows.

     The `problem` arrives attached to its grid (Runner does this in
     `_worker_task`). KAStarAgg reads `problem.goals` once into its
     own `_all_goals` list and never mutates the problem; we can
     safely build a fresh KAStarAgg instance per config on the same
     problem object.
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    k = len(problem.goals_rc)

    _log.info(f'start  ({domain}, {map_name}, k={k}) '
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
        rows.append(_snapshot(domain=domain,
                              map_name=map_name,
                              k=k,
                              is_lazy=is_lazy,
                              is_opt=is_opt,
                              store_vector=store_vector,
                              config=cfg,
                              algo=algo))

    total_elapsed = sum(r['elapsed_total'] for r in rows)
    _log.info(f'done   ({domain}, {map_name}, k={k}) '
              f'{len(_CONFIGS)} configs in {total_elapsed:.2f}s total')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_all_configs(path_drive_pkl_in: str,
                    path_drive_grids_in: str,
                    path_drive_csv_out: str,
                    workers: int = 10,
                    n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-AGG (Φ=`_AGG`) over all 8 param configs across every
     ProblemGrid in `path_drive_pkl_in`, parallelized over `workers`
     worker processes. Emit one CSV at `path_drive_csv_out` on Drive.

     `n_problems` slices the loaded problem list to the first N
     entries. None (default) processes all 500 -> 500 x 8 = 4000
     CSV rows. Toy example: N=50 -> 50 x 8 = 400 rows.

     `workers` is auto-clamped to `min(workers, n_tasks)` -- no point
     spawning idle worker processes that each hold the grids in RAM.

     Flow
       1. Download the detached-problems pickle and grids pickle to
          `/tmp/`.
       2. Load via `ProblemGrid.Store.load` (binds shared StateCell
          cache per grid).
       3. Optionally slice to `n_problems` for toy mode.
       4. Re-pickle the (possibly sliced) subset.
       5. Run `ProblemGrid.Runner.run` with the experiment callable.
       6. Flatten the per-problem result lists into CSV rows; write;
          upload.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'kastar_agg_all_configs: agg={_AGG}, '
              f'workers={workers}, n_problems={n_problems}')

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

        # 3. Optional toy-mode slice.
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

        # 4. Re-pickle the (possibly sliced) subset. __getstate__ drops
        # grid + state cache automatically, so the file stays light.
        with open(path_filt, 'wb') as f:
            pickle.dump(problems, f, protocol=pickle.HIGHEST_PROTOCOL)

        # 5. Run on the pool. Each worker loads `path_grids` once,
        # builds a shared per-grid StateCell cache, then processes its
        # share of the tasks (each task = one problem x N configs).
        effective_workers = min(workers, n_tasks)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'each task = 1 problem x {len(_CONFIGS):,} configs '
                  f'-> {n_tasks * len(_CONFIGS):,} kA*-AGG runs total')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_kastar_agg_all_configs,
            workers=effective_workers,
            chunksize=1)

        # 6. Flatten + write CSV + upload.
        rows = [row for task_rows in results for row in task_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} tasks x {len(_CONFIGS):,} '
                  f'configs); writing CSV')
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
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: process only the first N problems of the 500-problem
    # pickle (None == all 500). Useful for smoke-testing the pipeline.
    n_problems = None    # full run: set to None

    # Output path -- auto-suffix in toy mode so we never clobber the
    # full-run CSV.
    suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/OMSPP/'
                          f'kastar_agg_all_configs{suffix}.csv')

    run_all_configs(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
