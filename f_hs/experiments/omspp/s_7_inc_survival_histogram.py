"""
===============================================================================
 Script: dump KAStarInc's per-node SURVIVAL histogram, parallelized
 over a process pool (mirrors s_4's ProblemGrid.Runner structure).

 Purpose
   Visualize WHY INC's `cnt_h_update` stays small relative to AGG's
   `cnt_h_search` (and hence why INC ≪ AGG on `cnt_h_total`).

   `cnt_h_search` is definitional: INC computes h once per node per
   sub-search; AGG computes ≈|A|≈k per node. The open objection is
   about `cnt_h_update`: *if a node survived in OPEN across all k
   sub-searches, INC's per-transition refresh would re-price it ≈k
   times → ≈k h-calls for that node too, AGG-like.*

   survival[n] = #inter-sub-search transitions n was in OPEN
               = n's number of `cnt_h_update` h-calls
   sum(survival.values()) == cnt_h_update           (exact invariant)

   The histogram shows the tail (survive ≈k) is essentially empty —
   so `cnt_h_update` is small. That is the chart.

 Parallelism
   Built on `ProblemGrid.Runner` (ProcessPoolExecutor), exactly like
   `s_4_kastar_inc_extended.py`:
     - `workers` worker processes (default 10).
     - Each worker loads `Experiments/Grids/grids.pkl` ONCE, builds a
       shared per-grid StateCell cache, then processes its share of
       the 25 chains. Per-task IPC payload = light detached
       `ProblemGrid` only.
     - Work unit = 1 chain = 20 k-snapshots. 25 chains → 25 tasks.
   Survival tracing holds a dict over OPEN nodes (fringe-sized,
   ~hundreds) — negligible IPC/RAM on top of the plain INC run.

 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap bundle

 Output  (Drive)
   Experiments/OMSPP/inc_survival_histogram.csv
   Columns: domain, map, k, survival_count, num_nodes, fraction,
            cnt_h_update
   Long/tidy: per (domain, map, k) one row per distinct
   survival_count. Invariant per (domain, map, k):
   sum(survival_count * num_nodes) == cnt_h_update.

 Run (user executes):
   python -m f_hs.experiments.omspp.s_7_inc_survival_histogram
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

_CSV_COLUMNS = [
    'domain', 'map', 'k',
    'survival_count', 'num_nodes', 'fraction', 'cnt_h_update',
]

# k-checkpoints -- matches s_3_problems.py: range(10, 201, 10).
_KS = list(range(10, 201, 10))
_K_FINAL = _KS[-1]


# ── Heuristic (module-level so it's picklable for spawn workers) ────────────

def _h(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid -- bi-arg form expected by
     KAStarInc.
    ============================================================================
    """
    return float(s.distance(g))


# ── Snapshot helper ─────────────────────────────────────────────────────────

def _hist_rows(domain: str,
               map_name: str,
               k: int,
               algo: KAStarInc) -> list[dict]:
    """
    ========================================================================
     Flatten the cumulative survival histogram at checkpoint k into
     tidy CSV rows. Asserts the defining invariant
     sum(survival_count * num_nodes) == cnt_h_update.
    ========================================================================
    """
    hist = algo.survival_histogram
    total_nodes = sum(hist.values())
    cnt_h_update = algo.counters['cnt_h_update']
    assert sum(s * n for s, n in hist.items()) == cnt_h_update, (
        f'survival invariant broken on {domain}/{map_name} k={k}')
    return [{
        'domain':         domain,
        'map':            map_name,
        'k':              k,
        'survival_count': s,
        'num_nodes':      n,
        'fraction':       (n / total_nodes if total_nodes else 0.0),
        'cnt_h_update':   cnt_h_update,
    } for s, n in hist.items()]


# ── Worker experiment (module-level => picklable for ProcessPool) ──

def _experiment_inc_survival(problem: ProblemGrid) -> list[dict]:
    """
    ============================================================================
     Run one is_tracing=True INC chain on `problem` (carrying
     _K_FINAL goals): run([g1..g10]) then 19 extend()s, snapshotting
     the cumulative survival histogram at every k-checkpoint.

     `problem` arrives attached to its grid (Runner does this in its
     worker task). Returns the flattened histogram rows for all 20
     checkpoints of this chain.
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

    problem._goals = goals_all[:_KS[0]]
    algo = KAStarInc(problem=problem, h=_h, is_tracing=True)
    algo.run()
    rows = _hist_rows(domain, map_name, _KS[0], algo)

    for k_target in _KS[1:]:
        algo.extend(goals_all[k_target - 10:k_target])
        rows += _hist_rows(domain, map_name, k_target, algo)

    _log.info(f'done   ({domain}, {map_name}) '
              f'cnt_h_update@k{_K_FINAL}='
              f'{algo.counters["cnt_h_update"]:,}')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def run_survival_benchmark(path_drive_pkl_in: str,
                           path_drive_grids_in: str,
                           path_drive_csv_out: str,
                           workers: int = 10,
                           n_problems: int | None = None) -> None:
    """
    ============================================================================
     Run KAStarInc with `is_tracing=True` across the nested-k chains
     in `path_drive_pkl_in`, parallelized over `workers` processes,
     and emit the survival-histogram CSV to Drive.

     Same flow as `s_4.run_extended_benchmark`: download → Store.load
     → optional toy slice → filter to k=200 chains → re-pickle →
     ProblemGrid.Runner.run → flatten → upload. `workers` is
     auto-clamped to the chain count.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info(f'inc_survival_histogram: workers={workers}')

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
        drive.download(path_src=path_drive_grids_in,
                       path_dest=path_grids)

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
            pickle.dump(filtered, f,
                        protocol=pickle.HIGHEST_PROTOCOL)

        effective_workers = min(workers, n_chains)
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_chains={n_chains}); '
                  f'dispatching {n_chains:,} chains '
                  f'(each = {len(_KS):,} snapshots; chunksize=1)')
        results = ProblemGrid.Runner.run(
            path_problems=path_filt,
            path_grids=path_grids,
            experiment=_experiment_inc_survival,
            workers=effective_workers,
            chunksize=1)

        rows = [row for chain_rows in results for row in chain_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results):,} chains); writing CSV')
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
    # The __main__ guard is mandatory: spawn re-imports this module
    # in every worker; without it each worker re-launches the run.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: first N problems of the 500-problem pickle (None ==
    # all 500 → 25 chains × 20 k). Slice is BEFORE the k=200 filter.
    n_problems = None    # full run: None

    suffix = f'_toy{n_problems}' if n_problems is not None else ''
    path_drive_csv_out = (f'Experiments/OMSPP/'
                          f'inc_survival_histogram{suffix}.csv')

    run_survival_benchmark(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_problems=n_problems)
    _log.info('--- done ---')
