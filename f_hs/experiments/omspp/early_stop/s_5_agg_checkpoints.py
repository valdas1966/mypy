"""
===============================================================================
 Script: kA*-AGG mission-cancellation checkpoints.

 Early-stop framing -- a full k=200 OMSPP search is launched, then an
 external event cancels it at a progress milestone (r objectives
 completed). We price the cost ALREADY INCURRED at cancellation:
 expanded nodes, PEAK memory, runtime, as a function of r.

   r in {1, 50, 100, 150, 199}   (reach-rank of the completed goal)

 *** REQUIRES CORE HOOK (NOT YET MERGED) ***
   Unlike INC, kA*-AGG solves the full k=200 in ONE search and reaches
   goals one-at-a-time mid-loop; its on_goal event is recorder-based
   (post-hoc) and there is NO running-max memory tracker. So the
   per-goal snapshot CANNOT be captured externally. This runner reads:
       algo.checkpoints  -- list of {r, cnt_expanded, mem_peak, elapsed}
                            appended at each on_goal, where r is the
                            1-based REACH rank.
   populated by two flag-gated, zero-overhead-when-off instruments on
   KAStarAgg (mirroring the existing `is_tracing` / `is_timing` flags):
       is_checkpointing -- per-on_goal snapshot (light: one read/goal).
       is_mem_tracking  -- per-expansion running max of the slot model
                           m = |CLOSED| + |OPEN|*(1+|A|).
   Until that hook is merged, this script raises a clear error.

 Why PEAK, not end -- AGG's OPEN carries the active-goal h-vector and
 is non-monotone, so AGG's resident footprint peaks MID-search; the
 end-of-search reading under-counts. mem_peak is the running max over
 [0, r], captured per expansion.

 Metrics per checkpoint (row schema below)
   cnt_expanded  -- cumulative expanded nodes to the r-th goal (exact).
   mem_total     -- peak intrinsic slot count over [0, r]:
                    max_t |CLOSED| + |OPEN|*(1+|A|), |A| = CURRENT
                    active-goal count (shrinks as goals are reached).
                    Slot counts, not getsizeof bytes.
   elapsed_total -- cumulative wall-clock to the r-th goal (noisy).

 Two passes (mirrors early_stop/PLAN)
   Pass A  -- cnt_expanded + mem_total. is_mem_tracking=True (heavy,
              per-expansion) but is_timing=False so it never touches
              the clock. Deterministic; one run per config.
   Pass B  -- elapsed_total. is_mem_tracking=False (tracker OFF the
              clock), is_timing=True; rerun 3x, per-r MEDIAN taken.

 AGG config -- the single canonical aggregative version: kA*-MIN,
 lazy mode, is_opt=True, store_vector=True (the best from prior
 experiments). Only one config, so the CSV carries no `config` column.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle
   (filtered to the 25 k=200 problems)

 Output  (Drive)
   Experiments/OMSPP/early_stop/agg_checkpoints.csv

 Row schema (7 cols)
   domain, map, algo, r, cnt_expanded, mem_total, elapsed_total
   algo='agg' (the only AGG config; no config column).
-------------------------------------------------------------------------------
 Toy mode
   `n_problems` (None = all 500) slices BEFORE the k=200 filter, as in
   the parent s_5. N<20 strips every k=200 problem and raises. Toy
   output gets a `_toy{N}` suffix.
===============================================================================
"""
import os
import csv
import pickle
import tempfile
import logging
import statistics

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Φ aggregation. is_opt requires MIN or MAX; we pick MIN (as in s_5).
_AGG = 'MIN'

# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'algo',
    'r',
    'cnt_expanded',
    'mem_total',
    'elapsed_total',
]

# Cancellation points -- reach-rank of the completed goal. 199, not 200.
_RS = [1, 50, 100, 150, 199]

# Full problem size we filter to.
_K_FINAL = 200

# Timed repetitions for Pass B (per-r median of elapsed_total).
_TIMED_REPS = 3

# The single canonical AGG: kA*-MIN, lazy, opt, stored vector.
_IS_LAZY = True
_IS_OPT = True
_STORE_VECTOR = True


# ── Heuristic (module-level so it's picklable for spawn workers) ────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid -- bi-arg form expected by
     KAStarAgg.
    ============================================================================
    """
    return float(s.key.distance(g.key))


# ── Checkpoint extraction ────────────────────────────────────────────────────

def _require_hook(algo: KAStarAgg) -> None:
    """
    ========================================================================
     Fail loudly if the KAStarAgg checkpoint hook is not present. This
     runner is inert until the flag-gated `is_checkpointing` /
     `is_mem_tracking` instruments + `algo.checkpoints` are merged into
     core KAStarAgg.
    ========================================================================
    """
    if not hasattr(algo, 'checkpoints'):
        raise RuntimeError(
            'KAStarAgg has no `checkpoints` attribute -- the early-stop '
            'core hook (is_checkpointing / is_mem_tracking) is not yet '
            'merged. See this script header.')


def _pick(checkpoints: list[dict], field: str) -> dict[int, float]:
    """
    ========================================================================
     Map r -> field value for the r in _RS, reading the per-on_goal
     `checkpoints` list (keyed by 1-based reach rank `r`).
    ========================================================================
    """
    by_r = {cp['r']: cp for cp in checkpoints}
    out: dict[int, float] = {}
    for r in _RS:
        if r not in by_r:
            raise ValueError(
                f'checkpoint r={r} missing; run reached '
                f'{len(checkpoints)} goals')
        out[r] = by_r[r][field]
    return out


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ──

def _experiment_agg_checkpoints(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run the AGG config on one k=200 problem; emit 5 checkpoint rows
     (one per r). Pass A (untimed, mem-tracked) gives cnt_expanded +
     mem_total; Pass B (timed x3, no mem tracker) gives the per-r
     median elapsed_total.
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    _log.info(f'start  ({domain}, {map_name}) r={_RS}')

    # ── Pass A: cnt_expanded + mem_total (untimed, mem-tracked) ──
    algo = KAStarAgg(problem=problem, h=_h, agg=_AGG,
                     is_lazy=_IS_LAZY, is_opt=_IS_OPT,
                     store_vector=_STORE_VECTOR,
                     is_checkpointing=True,
                     is_mem_tracking=True,
                     is_timing=False)
    algo.run()
    _require_hook(algo)
    cnt = _pick(algo.checkpoints, 'cnt_expanded')
    mem = _pick(algo.checkpoints, 'mem_peak')

    # ── Pass B: elapsed_total (timed x3, mem tracker OFF clock) ──
    elapsed_reps: dict[int, list[float]] = {r: [] for r in _RS}
    for _ in range(_TIMED_REPS):
        a = KAStarAgg(problem=problem, h=_h, agg=_AGG,
                      is_lazy=_IS_LAZY, is_opt=_IS_OPT,
                      store_vector=_STORE_VECTOR,
                      is_checkpointing=True,
                      is_mem_tracking=False,
                      is_timing=True)
        a.run()
        ela = _pick(a.checkpoints, 'elapsed')
        for r in _RS:
            elapsed_reps[r].append(ela[r])

    rows = [{
        'domain':        domain,
        'map':           map_name,
        'algo':          'agg',
        'r':             r,
        'cnt_expanded':  cnt[r],
        'mem_total':     mem[r],
        'elapsed_total': round(statistics.median(elapsed_reps[r]), 6),
    } for r in _RS]

    _log.info(f'done   ({domain}, {map_name})')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_agg_checkpoints(path_drive_pkl_in: str,
                        path_drive_grids_in: str,
                        path_drive_csv_out: str,
                        workers: int = 10,
                        n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-AGG mission-cancellation checkpoints across the 25 k=200
     problems in `path_drive_pkl_in`, parallelized over `workers`
     processes. Emit one CSV at `path_drive_csv_out` on Drive.

     Flow mirrors `s_5_kastar_agg_all_configs.run_all_configs`, plus a
     k=200 filter (early-stop runs the full problem, not every k).
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'agg_checkpoints: agg={_AGG}, workers={workers}, r={_RS}')

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

        filtered = [p for p in problems
                    if len(p.goals_rc) == _K_FINAL]
        if not filtered:
            raise ValueError(
                f'no k={_K_FINAL} problems in the sliced set '
                f'(n_problems={n_problems!r}). Use n_problems >= 20.')
        n_tasks = len(filtered)
        _log.info(f'filtered: {n_tasks:,} k={_K_FINAL} problems')

        with open(path_filt, 'wb') as f:
            pickle.dump(filtered, f, protocol=pickle.HIGHEST_PROTOCOL)

        effective_workers = min(workers, n_tasks)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'each task = 1 problem x (1 + {_TIMED_REPS}) passes')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_agg_checkpoints,
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
    # The __main__ guard is mandatory: spawn workers re-import this
    # module, so the benchmark must not run at import time.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: first N problems (None == all). N>=20 keeps >=1 chain.
    n_problems = None

    toy_suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/OMSPP/early_stop/'
                          f'agg_checkpoints{toy_suffix}.csv')

    run_agg_checkpoints(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
