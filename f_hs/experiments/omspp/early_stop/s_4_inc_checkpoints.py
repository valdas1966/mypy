"""
===============================================================================
 Script: kA*-INC mission-cancellation checkpoints.

 Early-stop framing -- a full k=200 OMSPP search is launched, then an
 external event cancels it at a progress milestone (r objectives
 completed). We price the cost ALREADY INCURRED at cancellation:
 expanded nodes, peak memory, runtime, as a function of r.

   r in {1, 50, 100, 150, 199}   (reach-rank of the completed goal)

 Why INC needs no instrumentation
   kA*-INC is incremental: it solves goals in fixed order t_1..t_r by
   `run([t_1])` then `extend([t_i..])`. "r objectives completed" is
   therefore EXACTLY the state after extending the chain to r goals --
   a prefix of the full run. So we drive the same run()/extend() chain
   the parent `s_4_kastar_inc_extended.py` uses, but snapshot at the
   five r-breakpoints instead of every k=10.

 Metrics per checkpoint (row schema below)
   cnt_expanded  -- cumulative expanded nodes to the r-th goal (exact).
   mem_total     -- intrinsic slot count |CLOSED| + |OPEN|*(1+|A|).
                    INC carries no active-goal h-vector, so |A| = 0 and
                    mem_total = |CLOSED| + |OPEN|. INC stays light and
                    uniform, so its peak == end-of-checkpoint reading;
                    the snapshot at the checkpoint is the peak over
                    [0, r]. Read as intrinsic slot counts
                    (len of the live containers), NOT getsizeof bytes,
                    so the metric is machine-independent and reproducible.
   elapsed_total -- cumulative wall-clock to the r-th goal (noisy).

 Two passes (mirrors early_stop/PLAN)
   Pass A  -- cnt_expanded + mem_total. Deterministic; one chain build.
   Pass B  -- elapsed_total. The chain rebuilt 3x; per-r MEDIAN taken.
              No container reads on the clock -- timing stays clean.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle
   (filtered to the 25 k=200 chains)

 Output  (Drive)
   Experiments/OMSPP/early_stop/inc_checkpoints.csv

 Row schema (7 cols)
   domain, map, algo, r, cnt_expanded, mem_total, elapsed_total
   algo='inc' (the only INC config; no config column).
-------------------------------------------------------------------------------
 Toy mode
   `n_problems` (None = all 500) slices the pickle BEFORE the k=200
   filter, exactly as the parent s_4 does. N<20 strips every k=200
   chain and raises. Toy output gets a `_toy{N}` suffix.
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
from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


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

# Cancellation points -- reach-rank of the completed goal. The chain
# is grown to each of these and snapshotted. Note 199, not 200.
_RS = [1, 50, 100, 150, 199]

# Full chain length carried by a k=200 problem.
_K_FINAL = 200

# Timed repetitions for Pass B (per-r median of elapsed_total).
_TIMED_REPS = 3


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


# ── Chain driver ─────────────────────────────────────────────────────────────

def _mem_total(algo: KAStarInc) -> int:
    """
    ========================================================================
     Intrinsic slot count for INC at the current checkpoint:
     |CLOSED| + |OPEN| (|A| = 0 for INC). Reads live container lengths
     off the shared search state -- no bytes, no getsizeof.
    ========================================================================
    """
    ss = algo.search_state
    return len(ss.closed) + len(ss.frontier)


def _build_chain(problem: ProblemGrid, goals_all: list) -> KAStarInc:
    """
    ========================================================================
     Build the kA*-INC chain to the LAST breakpoint (199 goals) and
     return the live algo. Caller snapshots between stages via the
     generator form; this helper exists only for the timed pass, which
     does not need intermediate reads.
    ========================================================================
    """
    problem._goals = goals_all[:_RS[0]]
    algo = KAStarInc(problem=problem, h=_h)
    algo.run()
    prev = _RS[0]
    for r in _RS[1:]:
        algo.extend(goals_all[prev:r])
        prev = r
    return algo


def _experiment_inc_checkpoints(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run one k=200 chain and emit 5 checkpoint rows (one per r in _RS).

     Pass A -- build the chain once, snapshotting cnt_expanded + mem_total
               after the run / each extend.
     Pass B -- rebuild the chain `_TIMED_REPS` times, recording cumulative
               elapsed at each breakpoint; take the per-r median.
    ============================================================================
    """
    domain = problem.grid.domain
    map_name = problem.grid_name
    goals_all = list(problem._goals)
    if len(goals_all) != _K_FINAL:
        raise ValueError(
            f'expected {_K_FINAL} goals, got {len(goals_all)} on '
            f'{domain}/{map_name}')

    _log.info(f'start  ({domain}, {map_name}) r={_RS}')

    # ── Pass A: cnt_expanded + mem_total (deterministic) ────────────────
    problem._goals = goals_all[:_RS[0]]
    algo = KAStarInc(problem=problem, h=_h)
    algo.run()
    cnt: dict[int, int] = {_RS[0]: algo.counters['cnt_expanded']}
    mem: dict[int, int] = {_RS[0]: _mem_total(algo)}
    prev = _RS[0]
    for r in _RS[1:]:
        algo.extend(goals_all[prev:r])
        cnt[r] = algo.counters['cnt_expanded']
        mem[r] = _mem_total(algo)
        prev = r

    # ── Pass B: elapsed_total, median over _TIMED_REPS clean rebuilds ───
    elapsed_reps: dict[int, list[float]] = {r: [] for r in _RS}
    for _ in range(_TIMED_REPS):
        problem._goals = goals_all[:_RS[0]]
        a = KAStarInc(problem=problem, h=_h)
        a.run()
        elapsed_reps[_RS[0]].append(a.elapsed)
        p = _RS[0]
        for r in _RS[1:]:
            a.extend(goals_all[p:r])
            elapsed_reps[r].append(a.elapsed)
            p = r

    rows = [{
        'domain':        domain,
        'map':           map_name,
        'algo':          'inc',
        'r':             r,
        'cnt_expanded':  cnt[r],
        'mem_total':     mem[r],
        'elapsed_total': round(statistics.median(elapsed_reps[r]), 6),
    } for r in _RS]

    _log.info(f'done   ({domain}, {map_name}) '
              f'expanded@r199={cnt[_RS[-1]]:,} '
              f'mem@r1={mem[_RS[0]]:,}')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_inc_checkpoints(path_drive_pkl_in: str,
                        path_drive_grids_in: str,
                        path_drive_csv_out: str,
                        workers: int = 10,
                        n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run kA*-INC mission-cancellation checkpoints across the 25 k=200
     chains in `path_drive_pkl_in`, parallelized over `workers`
     processes. Emit one CSV at `path_drive_csv_out` on Drive.

     Flow mirrors `s_4_kastar_inc_extended.run_extended_benchmark`:
       download -> load -> (toy slice) -> filter k=200 -> re-pickle ->
       Runner.run -> flatten -> write CSV -> upload.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'inc_checkpoints: workers={workers}, r={_RS}')

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
        n_chains = len(filtered)
        _log.info(f'filtered: {n_chains:,} k={_K_FINAL} chains')

        with open(path_filt, 'wb') as f:
            pickle.dump(filtered, f, protocol=pickle.HIGHEST_PROTOCOL)

        effective_workers = min(workers, n_chains)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_chains={n_chains}); '
                  f'each chain = {len(_RS):,} checkpoints')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_inc_checkpoints,
            workers=effective_workers,
            chunksize=1)

        rows = [row for chain_rows in results for row in chain_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} chains x {len(_RS):,} r); '
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
    # The __main__ guard is mandatory: spawn workers re-import this
    # module, so the benchmark must not run at import time.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: first N problems (None == all). N>=20 keeps >=1 chain.
    n_problems = None

    toy_suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/OMSPP/early_stop/'
                          f'inc_checkpoints{toy_suffix}.csv')

    run_inc_checkpoints(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
