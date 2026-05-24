"""
===============================================================================
 Script: run AStarIncMOSPP across the 25 maps of
 `Experiments/OMSPP/i_3_problems.pkl` as NESTED k-chains, for
 ONE fixed algorithm config. Parallelized over a process pool;
 emits one CSV row per (map, k) stage to Drive.

 The 500 OMSPP problems are 25 maps x 20 k-values
 (k = 10, 20, ..., 200). For a given map the goal sets are
 prefix-nested: goals(k) is a superset of goals(k-10). After
 the OM<->MO flip (`ProblemSPP.flipped()`, exact on the
 undirected grids) this becomes nested MOSPP START sets that
 all share ONE goal (the pinned OMSPP start).
-------------------------------------------------------------------------------
 Nested-chain run -- the incremental win, exploited
   Per map, instead of 20 independent AStarIncMOSPP runs, ONE
   AStarIncMOSPP solves the whole k=10..200 chain:
     run()    on the k=10 MOSPP problem      -> snapshot row
     extend() with the +10 new starts  x19   -> 19 more rows
   AStarIncMOSPP composes `ExtendableMOSPP`; its goal-anchored
   cache / bounds carry across every extend (the goal is
   fixed), so the k=200 stage reuses everything k=10..190
   discovered. Per map: ~200 sub-searches total, not the
   ~2,100 of 20 independent runs -- a ~10x cut. Still 500
   rows (25 maps x 20 stages).

 Row semantics -- CUMULATIVE
   The row for stage k carries the counters / elapsed
   ACCUMULATED over sub-searches 1..k (the cost to reach k
   starts incrementally). Diff consecutive rows of one map
   for the marginal cost of a +10 batch. `m` is the
   cumulative start count (= the OMSPP k).
-------------------------------------------------------------------------------
 Algorithm config -- three explicit run parameters
   rule_bpmx   : {None, '1', '2', '3', 'CASCADE'}. The inner-
                 AStarBPMX Felner rule. None = in-search BPMX
                 OFF.
   depth_bpmx  : int >= 1, or None = BPMX to convergence. The
                 in-search BPMX cascade depth; ignored when
                 rule_bpmx is None.
   depth_prop  : 0 = no pre-search pathmax propagation;
                 int >= 1 = propagate to that depth;
                 None = propagate to convergence. Decodes to
                 the algorithm's (propagate, propagate_depth)
                 pair (mirrors the depth_bpmx convention):
                   depth_prop == 0    -> propagate=False
                   depth_prop == N    -> propagate=True, N
                   depth_prop is None -> propagate=True, None

   Held fixed:
     order_starts='given' -- no reordering, so run() and the
       19 extend()s process the chain coherently in problem
       order (the order the nested chain is built in).
     carry_cache=True, carry_bounds=False -- the on-path
       cache is the SOLE carried reuse store (the oracle's
       "only cached" Group-C family; see
       `f_hs/algo/i_1_mospp/i_1_astar_inc/study/oracle.py`).

 One invocation = one config = one CSV. To sweep a knob, run
 the script repeatedly; each run's CSV is named by its config
 (see `_csv_filename`) so runs never clobber each other.
-------------------------------------------------------------------------------
 Work unit -- one task per MAP (one nested k-chain)
   `_MapChain` bundles a map's 20 detached problems (sorted by
   m) into a single Runner task: 25 tasks -> 25 chains ->
   500 rows.

 Parallelism
   Built on `ProblemGrid.Runner` (ProcessPoolExecutor):
     - `workers` worker processes (default 10).
     - Each worker loads `Experiments/Grids/grids.pkl` once at
       init; the heavy GridMap objects + a shared StateCell
       cache per grid stay in worker memory.
     - The config travels into the workers via a
       `functools.partial` around the module-level experiment
       fn (picklable -- a plain closure would not ship).
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/i_3_problems.pkl   -- 500 detached
                                           ProblemGrid
   Experiments/Grids/grids.pkl          -- name -> GridMap

 Output  (Drive)
   Experiments/MOSPP/
     astar_inc_nested__rule_{R}__bpmx_{B}__prop_{P}.csv
   R = rule_bpmx (None -> 'none'), B = depth_bpmx
   (None -> 'inf'), P = depth_prop (None -> 'inf'). Toy runs
   get a trailing `_toy{N}`.

 Toy mode
   `n_maps` (None = all 25) slices to the first N maps ->
   N x 20 rows. The CSV gets a `_toy{N}` suffix so a smoke
   run never clobbers the full-run CSV.

 Compute note
   A full run is 25 nested chains, ~200 AStarIncMOSPP
   sub-searches each (~5,000 total). Give it cores.
===============================================================================
"""
import os
import csv
import pickle
import tempfile
import logging
from collections import defaultdict
from functools import partial

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
# 'given' order: run() + every extend() process the chain in problem
# order -- the consistent policy for an extend()-based nested chain.
_ORDER_STARTS = 'given'

# Valid in-search BPMX rules (mirrors BPMXMixin._VALID_RULE_BPMX);
# used by `_validate_config` to fail fast before the pool spins up.
_VALID_RULES_BPMX = (None, '1', '2', '3', 'CASCADE')


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain', 'map', 'm', 'rule_bpmx', 'depth_bpmx', 'depth_prop',
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
    ========================================================================
     Manhattan heuristic for ProblemGrid StateCells -- bi-arg form
     `h(state, goal)` expected by AStarIncMOSPP.
    ========================================================================
    """
    return float(s.distance(g))


# ── Runner task-unit adapter — one map's nested k-chain ─────────────────────

class _MapChain:
    """
    ========================================================================
     Runner task-unit adapter: one map's nested k-chain.

     Holds the chain of detached `ProblemGrid` problems for a
     single map (k = 10, 20, ..., 200; nested goal sets, one
     shared OMSPP start), sorted ascending by m. Exposes the
     two members `ProblemGrid.Runner._worker_task` invokes --
     `grid_name` and `attach(grid, states)` -- so a whole
     chain rides the UNMODIFIED Runner as ONE task: the worker
     attaches every problem in the chain to the same grid +
     shared StateCell cache, then hands the chain to the
     experiment fn. Picklable (holds only detached problems).
    ========================================================================
    """

    def __init__(self, problems: list[ProblemGrid]) -> None:
        self._problems = problems

    @property
    def grid_name(self) -> str:
        """
        ====================================================================
         Stable grid id -- every problem in the chain shares it.
        ====================================================================
        """
        return self._problems[0].grid_name

    def attach(self, grid, states=None) -> None:
        """
        ====================================================================
         Attach every problem in the chain to the one shared
         grid + StateCell cache. Signature matches the
         `problem.attach(grid=, states=)` call in
         `ProblemGrid.Runner._worker_task`.
        ====================================================================
        """
        for p in self._problems:
            p.attach(grid=grid, states=states)

    def __iter__(self):
        """
        ====================================================================
         Iterate the chain's problems, ascending m.
        ====================================================================
        """
        return iter(self._problems)


# ── CSV filename ────────────────────────────────────────────────────────────

def _csv_filename(rule_bpmx: str | None,
                  depth_bpmx: int | None,
                  depth_prop: int | None,
                  n_maps: int | None) -> str:
    """
    ========================================================================
     Build the output CSV filename, encoding the run config so
     repeated single-config runs never clobber each other:
       astar_inc_nested__rule_{R}__bpmx_{B}__prop_{P}[_toy{N}].csv
     None renders as 'none' for the rule and 'inf' for either
     depth. A toy run appends `_toy{N}` (N = n_maps).
    ========================================================================
    """
    r = rule_bpmx if rule_bpmx is not None else 'none'
    b = 'inf' if depth_bpmx is None else depth_bpmx
    p = 'inf' if depth_prop is None else depth_prop
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return (f'astar_inc_nested__rule_{r}__bpmx_{b}'
            f'__prop_{p}{toy}.csv')


# ── Config validation ───────────────────────────────────────────────────────

def _validate_config(rule_bpmx: str | None,
                     depth_bpmx: int | None,
                     depth_prop: int | None) -> None:
    """
    ========================================================================
     Fail fast on a bad config BEFORE the pool spins up -- a
     bad value would otherwise raise identically in all 25
     tasks. The inner AStarIncMOSPP still enforces the
     rule_bpmx='2' => depth_bpmx==1 cross-constraint at
     construction.
    ========================================================================
    """
    if rule_bpmx not in _VALID_RULES_BPMX:
        raise ValueError(
            f'rule_bpmx must be one of {_VALID_RULES_BPMX}; '
            f'got {rule_bpmx!r}')
    if depth_bpmx is not None and depth_bpmx < 1:
        raise ValueError(
            f'depth_bpmx must be an int >= 1, or None '
            f'(= BPMX to convergence); got {depth_bpmx!r}. '
            f'For in-search BPMX OFF set rule_bpmx=None.')
    if depth_prop is not None and depth_prop < 0:
        raise ValueError(
            f'depth_prop must be 0 (no propagation), an int >= 1 '
            f'(propagate to that depth), or None (propagate to '
            f'convergence); got {depth_prop!r}.')


# ── Chain building + nesting verification ───────────────────────────────────

def _build_chains(problems: list[ProblemGrid]
                  ) -> dict[str, list[ProblemGrid]]:
    """
    ========================================================================
     Group the flat problem list into per-map chains keyed by
     `grid_name`, each sorted ascending by m (= number of
     OMSPP goals).
    ========================================================================
    """
    chains: dict[str, list[ProblemGrid]] = defaultdict(list)
    for p in problems:
        chains[p.grid_name].append(p)
    for chain in chains.values():
        chain.sort(key=lambda p: len(p.goals_rc))
    return chains


def _verify_chains(chains: dict[str, list[ProblemGrid]]) -> None:
    """
    ========================================================================
     Assert the nested-chain preconditions for every map:
       - all problems on a map share ONE OMSPP start (=> after
         the flip, one shared MOSPP goal -- required by
         AStarIncMOSPP);
       - the OMSPP goal sets are prefix-nested:
         goals(k) is a superset of goals(k-10) (=> after the
         flip, prefix-extending MOSPP start sets).
     Raises ValueError naming the offending map on failure.
    ========================================================================
    """
    for name, chain in chains.items():
        starts = {tuple(p.starts_rc) for p in chain}
        if len(starts) != 1:
            raise ValueError(
                f'chain {name!r}: problems do not share one '
                f'OMSPP start (=> not one MOSPP goal after the '
                f'flip): {starts}')
        for a, b in zip(chain, chain[1:]):
            if not set(a.goals_rc) <= set(b.goals_rc):
                raise ValueError(
                    f'chain {name!r}: goal sets not nested at '
                    f'm={len(a.goals_rc)} -> m={len(b.goals_rc)}; '
                    f'the nested-chain experiment requires '
                    f'per-map prefix-superset goal sets.')


# ── Row builder ─────────────────────────────────────────────────────────────

def _row(domain: str,
         map_name: str,
         m: int,
         rule_bpmx: str | None,
         depth_bpmx: int | None,
         depth_prop: int | None,
         algo: AStarIncMOSPP) -> dict:
    """
    ========================================================================
     Build one CSV row from the AStarIncMOSPP at a chain
     stage: its (CUMULATIVE) counters + elapsed buckets,
     tagged with the map identity, the stage start-count `m`,
     and the run config. None renders as 'none' (rule) /
     'inf' (either depth) so the columns stay flat across
     CSVs.
    ========================================================================
    """
    c = dict(algo.counters.items())
    row = {
        'domain':         domain,
        'map':            map_name,
        'm':              m,
        'rule_bpmx':      'none' if rule_bpmx is None else rule_bpmx,
        'depth_bpmx':     'inf' if depth_bpmx is None else depth_bpmx,
        'depth_prop':     'inf' if depth_prop is None else depth_prop,
        'elapsed_total':  round(algo.elapsed, 6),
        'elapsed_search': round(algo.elapsed_search, 6),
        'elapsed_update': round(algo.elapsed_update, 6),
    }
    for name in _COUNTER_NAMES:
        row[name] = c.get(name, 0)
    return row


# ── Worker experiment (module-level => picklable for ProcessPoolExecutor) ───

def _experiment_astar_inc_chain(chain: _MapChain,
                                rule_bpmx: str | None,
                                depth_bpmx: int | None,
                                depth_prop: int | None
                                ) -> list[dict]:
    """
    ========================================================================
     Solve one map's nested k-chain with a single
     AStarIncMOSPP, for the given config. Returns one row per
     k-stage (20 rows).

     `chain` arrives attached (the Runner attaches every
     problem). Each OMSPP-shaped ProblemGrid is `flipped()`
     into a MOSPP problem (k starts, 1 goal). The first
     (smallest-k) problem seeds `run()`; each subsequent
     problem contributes its +10 new starts via `extend()`.
     Because the chain is nested and the goal is fixed, the
     carried cache / bounds accumulate across the whole
     chain.

     `depth_prop` is decoded to the algorithm's (propagate,
     propagate_depth) pair:
       0      -> propagate=False (no pre-search propagation)
       N >= 1 -> propagate=True,  propagate_depth=N
       None   -> propagate=True,  propagate_depth=None
    ========================================================================
    """
    problems = list(chain)               # ascending m
    domain = getattr(problems[0].grid, 'domain', '') or ''
    map_name = problems[0].grid_name
    # Decode depth_prop -> (propagate, propagate_depth).
    if depth_prop == 0:
        propagate, propagate_depth = False, None
    else:
        propagate, propagate_depth = True, depth_prop
    # Flip every OMSPP problem -> MOSPP (k starts, 1 goal).
    flipped = [p.flipped() for p in problems]
    _log.info(f'start  ({domain}, {map_name}) chain '
              f'm={len(flipped[0].starts)}..'
              f'{len(flipped[-1].starts)}')

    # Seed with the smallest-k MOSPP problem.
    algo = AStarIncMOSPP(
        problem=flipped[0],
        h=_h,
        is_recording=False,
        is_timing=True,
        order_starts=_ORDER_STARTS,
        carry_cache=_CARRY_CACHE,
        carry_bounds=_CARRY_BOUNDS,
        propagate=propagate,
        propagate_depth=propagate_depth,
        rule_bpmx=rule_bpmx,
        depth_bpmx=depth_bpmx,
    )
    algo.run()
    rows = [_row(domain, map_name, len(flipped[0].starts),
                 rule_bpmx, depth_bpmx, depth_prop, algo)]

    # Extend by each subsequent problem's +10 genuinely-new
    # starts; snapshot a (cumulative) row per stage.
    seen = set(flipped[0].starts)
    for fp in flipped[1:]:
        new = [s for s in fp.starts if s not in seen]
        if new:
            algo.extend(new)
            seen.update(new)
        rows.append(_row(domain, map_name, len(fp.starts),
                         rule_bpmx, depth_bpmx, depth_prop, algo))

    _log.info(f'done   ({domain}, {map_name}) {len(rows)} rows '
              f'elapsed={algo.elapsed:.2f}s')
    return rows


# ── Public API ──────────────────────────────────────────────────────────────

def run_astar_inc(path_drive_pkl_in: str,
                  path_drive_grids_in: str,
                  path_drive_csv_out: str,
                  rule_bpmx: str | None,
                  depth_bpmx: int | None,
                  depth_prop: int | None,
                  workers: int = 10,
                  n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run AStarIncMOSPP across every map in `path_drive_pkl_in`
     as a NESTED k-chain (OMSPP problems flipped to MOSPP),
     for ONE config (`rule_bpmx`, `depth_bpmx`, `depth_prop`).
     Parallelized over `workers` processes -- one task per
     map. Emits one CSV to `path_drive_csv_out` on Drive --
     one (cumulative) row per (map, k) stage.

     `n_maps` slices the chain list to the first N maps (toy /
     smoke mode); None processes all of them. `workers` is
     clamped to `min(workers, n_maps_effective)`.

     Flow:
       1. Validate the config; fail fast before the pool.
       2. Download the OMSPP problems pickle + grids pickle.
       3. Group problems into per-map chains; verify the
          nested-chain preconditions; optionally toy-slice;
          wrap each chain in a `_MapChain` and re-pickle for
          the Runner.
       4. `ProblemGrid.Runner.run` dispatches one task per
          chain; each worker attaches the chain, runs the
          `run()` + `extend()` sequence. The config ships
          into the workers via a `functools.partial`.
       5. Flatten the per-chain row lists; write + upload the
          CSV.
    ========================================================================
    """
    _validate_config(rule_bpmx=rule_bpmx,
                     depth_bpmx=depth_bpmx,
                     depth_prop=depth_prop)
    if n_maps is not None and n_maps < 1:
        raise ValueError(f'n_maps must be >= 1; got {n_maps}')
    drive = Drive.Factory.valdas()
    _log.info(f'astar_inc nested: workers={workers}, '
              f'rule_bpmx={rule_bpmx!r}, depth_bpmx={depth_bpmx!r}, '
              f'depth_prop={depth_prop!r}')

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

        # 2. Load, group into per-map chains, verify nesting.
        with open(path_in, 'rb') as f:
            problems = pickle.load(f)
        _log.info(f'loaded {len(problems):,} problems')
        chains = _build_chains(problems)
        _verify_chains(chains)
        chain_units = [_MapChain(c) for c in chains.values()]
        _log.info(f'built {len(chain_units)} per-map chains '
                  f'(nesting verified)')
        if n_maps is not None:
            chain_units = chain_units[:n_maps]
            _log.info(f'toy mode: sliced to first '
                      f'{len(chain_units)} maps')
        with open(path_run, 'wb') as f:
            pickle.dump(chain_units, f,
                        protocol=pickle.HIGHEST_PROTOCOL)

        # 3. Dispatch one task per chain over the worker pool.
        #    The config rides into each worker on a picklable
        #    partial.
        n_tasks = len(chain_units)
        effective_workers = max(1, min(workers, n_tasks))
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'{n_tasks} nested chains (chunksize=1)')
        experiment = partial(_experiment_astar_inc_chain,
                             rule_bpmx=rule_bpmx,
                             depth_bpmx=depth_bpmx,
                             depth_prop=depth_prop)
        results = ProblemGrid.Runner.run(
            path_problems=path_run,
            path_grids=path_grids,
            experiment=experiment,
            workers=effective_workers,
            chunksize=1)

        # 4. Flatten the per-chain row lists + write CSV + upload.
        rows = [r for chain_rows in results for r in chain_rows]
        _log.info(f'received {len(rows):,} rows '
                  f'({len(results)} chains); writing CSV')
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
    # Without the guard, every worker would re-launch the run.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    workers = 10

    # Toy mode: process only the first N of the 25 maps
    # (None == all 25). Useful for smoke-testing before a full
    # run -- N=1 is one nested chain (~200 sub-searches).
    n_maps = None

    # ── Algorithm config — one run, one config, one CSV ─────────────────────
    # rule_bpmx  : {None, '1', '2', '3', 'CASCADE'}; None = BPMX off.
    # depth_bpmx : int >= 1, or None = BPMX to convergence.
    # depth_prop : 0 = no propagation; int >= 1 = propagate to that
    #              depth; None = propagate to convergence.
    rule_bpmx = '3'
    depth_bpmx = 1
    depth_prop = 0

    # Output path — encodes the config so repeated single-config
    # runs never clobber each other; `_toy{N}` suffix in toy mode.
    path_drive_csv_out = (
        f'Experiments/MOSPP/'
        f'{_csv_filename(rule_bpmx, depth_bpmx, depth_prop, n_maps)}')

    run_astar_inc(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        rule_bpmx=rule_bpmx,
        depth_bpmx=depth_bpmx,
        depth_prop=depth_prop,
        workers=workers,
        n_maps=n_maps)
    _log.info('--- done ---')
