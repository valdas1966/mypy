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
     carry_cache -- a PER-RUN knob (default True: the on-path
       cache is carried). The `inc_adapt_nocache` driver sets
       False to turn the cache OFF (pure Adaptive A*, ADAPT-only)
       -- its CSV gets a `_cacheoff` token.
     adaptive_h -- now a PER-RUN knob (default False: the cache
       is the SOLE carried reuse store, the oracle's "only
       cached" Group-C family). The `inc_adapt` driver sets True
       to ADD the Adaptive A* (`C_i-g_i`) CLOSED-list bound store
       ON TOP of the cache; see
       `f_hs/algo/i_1_mospp/i_1_astar_inc/study/oracle.py`.

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
   Results/
     astar_inc_nested_rule_{R}_bpmx_{B}_prop_{P}[_adapt_1].csv
   R = rule_bpmx (None -> 'none'), B = depth_bpmx
   (None -> 'inf'), P = depth_prop (None -> 'inf'). Adaptive
   runs (adaptive_h=True) get an `_adapt_1` token; toy runs
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
from f_hs.algo.i_1_mospp.i_1_astar_flip import AStarFlipMOSPP
from f_hs.algo.i_1_mospp import (
    AStarRepMOSPP, BFSFlipMOSPP, DijkstraFlipMOSPP,
)


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Fixed algorithm config ──────────────────────────────────────────────────
# "only cached": carry the on-path cache across sub-searches. `_ADAPTIVE_H`
# is the DEFAULT for the per-run `adaptive_h` knob (False = the cache is the
# sole reuse store); the `inc_adapt` driver passes adaptive_h=True to ADD
# the Adaptive A* (C_i-g_i) CLOSED-list bound store on top of the cache.
_CARRY_CACHE = True
_ADAPTIVE_H = False
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
    'cnt_adapt_attempts', 'cnt_adapt_lifts',
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
    return float(s.key.distance(g.key))


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
                  n_maps: int | None,
                  adaptive_h: bool = False,
                  carry_cache: bool = True) -> str:
    """
    ========================================================================
     Build the output CSV filename, encoding the run config so
     repeated single-config runs never clobber each other:
       astar_inc_nested_rule_{R}_bpmx_{B}_prop_{P}[_adapt_1][_cacheoff][_toy{N}].csv
     None renders as 'none' for the rule and 'inf' for either
     depth. `adaptive_h=True` inserts an `_adapt_1` token (so an
     adaptive run never clobbers the non-adaptive run of the same
     rule/depth/prop -- the non-adaptive names carry no token).
     `carry_cache=False` inserts a `_cacheoff` token (so an
     ADAPT-on / CACHE-off run -- pure Koenig Adaptive A*, the
     missing cache-off cell of the 2x2 ablation -- never clobbers
     the cache-on run of the same rule/depth/prop/adapt). A toy run
     appends a trailing `_toy{N}` (N = n_maps), kept LAST so
     `s_4._is_results_csv` still detects + skips smoke runs.
    ========================================================================
    """
    r = rule_bpmx if rule_bpmx is not None else 'none'
    b = 'inf' if depth_bpmx is None else depth_bpmx
    p = 'inf' if depth_prop is None else depth_prop
    adapt = '_adapt_1' if adaptive_h else ''
    cacheoff = '' if carry_cache else '_cacheoff'
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return (f'astar_inc_nested_rule_{r}_bpmx_{b}'
            f'_prop_{p}{adapt}{cacheoff}{toy}.csv')


def _csv_filename_rep(n_maps: int | None) -> str:
    """
    ========================================================================
     Output CSV filename for the AStarRepMOSPP baseline (single
     config -- no rule / depth ladder):
       astar_rep_nested[_toy{N}].csv
    ========================================================================
    """
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return f'astar_rep_nested{toy}.csv'


def _csv_filename_flip(n_maps: int | None) -> str:
    """
    ========================================================================
     Output CSV filename for the AStarFlipMOSPP solver (MOSPP
     via flip-to-OMSPP incremental kA*; single config):
       astar_flip_nested[_toy{N}].csv
     `astar_`-prefixed + `nested` so `s_4._is_results_csv` picks
     it up; `s_4._algo_of` tags it `flip`.
    ========================================================================
    """
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return f'astar_flip_nested{toy}.csv'


def _csv_filename_bfs_flip(n_maps: int | None) -> str:
    """
    ========================================================================
     Output CSV filename for the BFSFlipMOSPP solver (MOSPP via
     flip-to-OMSPP backward BFS; single config):
       bfs_flip_nested[_toy{N}].csv
     `nested` + the `bfs_flip` prefix so `s_4._is_results_csv`
     picks it up; `s_4._algo_of` tags it `bfs`.
    ========================================================================
    """
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return f'bfs_flip_nested{toy}.csv'


def _csv_filename_dijkstra_flip(n_maps: int | None) -> str:
    """
    ========================================================================
     Output CSV filename for the DijkstraFlipMOSPP solver (MOSPP
     via flip-to-OMSPP backward Dijkstra; single config):
       dijkstra_flip_nested[_toy{N}].csv
     `nested` + the `dijkstra_flip` prefix so `s_4._is_results_csv`
     picks it up; `s_4._algo_of` tags it `dijkstra`.
    ========================================================================
    """
    toy = f'_toy{n_maps}' if n_maps is not None else ''
    return f'dijkstra_flip_nested{toy}.csv'


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
                                depth_prop: int | None,
                                adaptive_h: bool = _ADAPTIVE_H,
                                carry_cache: bool = _CARRY_CACHE
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
        carry_cache=carry_cache,
        adaptive_h=adaptive_h,
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


def _experiment_astar_rep_chain(chain: _MapChain) -> list[dict]:
    """
    ========================================================================
     Solve one map's nested k-chain with a SINGLE AStarRepMOSPP
     (the no-sharing baseline), exploiting prefix reuse. `run()`
     the smallest-k MOSPP instance, then `extend()` by each
     subsequent stage's +10 genuinely-new starts. Rep shares NO
     state across sub-searches, but `extend()` still runs each
     start's independent A* EXACTLY ONCE across the whole chain
     (it never re-solves the prefix), so the chain costs the same
     as 20 from-scratch runs would in total -- minus the
     redundant prefix re-solves a per-k loop would incur.

     Returns one (cumulative) row per k-stage (20 rows). Reuses
     the Inc `_row` builder with a None BPMX config: the rule /
     depth columns render 'none' / 'inf', and Rep's absent
     counters (`cnt_prop_*`, `cnt_bpmx_*`, `cnt_cache_hits_at_init`,
     `mem_cache`, `mem_bounds`) default to 0 -- keeping the CSV
     schema identical to the Inc runs for easy comparison.
    ========================================================================
    """
    problems = list(chain)               # ascending m
    domain = getattr(problems[0].grid, 'domain', '') or ''
    map_name = problems[0].grid_name
    flipped = [p.flipped() for p in problems]
    _log.info(f'start  REP ({domain}, {map_name}) chain '
              f'm={len(flipped[0].starts)}..'
              f'{len(flipped[-1].starts)}')

    # Seed with the smallest-k MOSPP problem.
    algo = AStarRepMOSPP(
        problem=flipped[0],
        h=_h,
        is_recording=False,
        is_timing=True,
    )
    algo.run()
    rows = [_row(domain, map_name, len(flipped[0].starts),
                 None, None, None, algo)]

    # Extend by each subsequent problem's +10 genuinely-new
    # starts; snapshot a (cumulative) row per stage.
    seen = set(flipped[0].starts)
    for fp in flipped[1:]:
        new = [s for s in fp.starts if s not in seen]
        if new:
            algo.extend(new)
            seen.update(new)
        rows.append(_row(domain, map_name, len(fp.starts),
                         None, None, None, algo))

    _log.info(f'done   REP ({domain}, {map_name}) {len(rows)} rows '
              f'elapsed={algo.elapsed:.2f}s')
    return rows


def _experiment_astar_flip_chain(chain: _MapChain) -> list[dict]:
    """
    ========================================================================
     Solve one map's nested k-chain with a SINGLE AStarFlipMOSPP
     -- MOSPP via the axis-swap (flip to OMSPP) + the incremental
     kA* solver, which grows ONE shared search tree OUTWARD from
     the shared goal to reach all starts (the OMSPP-side mirror
     of AStarIncMOSPP's forward reuse). `run()` the smallest-k
     MOSPP instance, then `extend()` by each stage's +10
     genuinely-new starts (the inner kA*_inc appends them as new
     OMSPP goals and keeps growing the one tree).

     Returns one (cumulative) row per k-stage (20 rows). Reuses
     the Inc `_row` builder with a None BPMX/prop config -- this
     solver has no BPMX / propagation / adaptive / cache-hit
     counters, so those columns default to 0 (like the Rep
     baseline). `cnt_h_update` (the inter-sub-search refresh
     cost) is exposed on the algo but not in `_CSV_COLUMNS`, so
     it is dropped from the CSV by design.

     Precondition: undirected, consistent-h grids (the flip is
     exact only there) -- satisfied by the experiment grids.
    ========================================================================
    """
    problems = list(chain)               # ascending m
    domain = getattr(problems[0].grid, 'domain', '') or ''
    map_name = problems[0].grid_name
    flipped = [p.flipped() for p in problems]
    _log.info(f'start  FLIP ({domain}, {map_name}) chain '
              f'm={len(flipped[0].starts)}..'
              f'{len(flipped[-1].starts)}')

    # Seed with the smallest-k MOSPP problem.
    algo = AStarFlipMOSPP(
        problem=flipped[0],
        h=_h,
        is_recording=False,
        is_timing=True,
    )
    algo.run()
    rows = [_row(domain, map_name, len(flipped[0].starts),
                 None, None, None, algo)]

    # Extend by each subsequent problem's +10 genuinely-new
    # starts; snapshot a (cumulative) row per stage.
    seen = set(flipped[0].starts)
    for fp in flipped[1:]:
        new = [s for s in fp.starts if s not in seen]
        if new:
            algo.extend(new)
            seen.update(new)
        rows.append(_row(domain, map_name, len(fp.starts),
                         None, None, None, algo))

    _log.info(f'done   FLIP ({domain}, {map_name}) {len(rows)} rows '
              f'elapsed={algo.elapsed:.2f}s')
    return rows


def _experiment_bfs_flip_chain(chain: _MapChain) -> list[dict]:
    """
    ========================================================================
     Solve one map's nested k-chain with BFSFlipMOSPP -- MOSPP via
     the axis-swap (flip to OMSPP) + a single backward BFS pass
     from the shared goal that reaches ALL k starts (goals after
     the flip) in one sweep.

     INDEPENDENT per-k runs (NOT run()+extend): BFSFlipMOSPP has no
     `extend()` -- one backward BFS already reaches every start, so
     there is no per-start sub-search to amortize. Each k-stage is
     therefore a fresh from-scratch BFSFlipMOSPP on that stage's
     MOSPP problem (k starts, 1 goal). The per-row metrics stay
     apples-to-apples with the incremental algos: the cost to reach
     the k-th start with one reverse BFS is identical whether the
     search is grown incrementally or restarted (BFS expands the
     same node set to reach a given start); only TOTAL experiment
     compute differs (each k re-explores the prefix). Memory is the
     node-count |OPEN|+|CLOSED| at completion and `elapsed` includes
     the flip + re-key, both via the shared `_row` builder.

     Returns one row per k-stage (20 rows). BFS has no BPMX / prop /
     adaptive / cache / heuristic counters, so those columns default
     to 0 (like the rep baseline).

     Precondition: undirected, UNIFORM-weight grids (BFS depth =
     optimal cost) -- satisfied by the experiment grids.
    ========================================================================
    """
    problems = list(chain)               # ascending m, OMSPP-shaped
    domain = getattr(problems[0].grid, 'domain', '') or ''
    map_name = problems[0].grid_name
    flipped = [p.flipped() for p in problems]
    _log.info(f'start  BFS  ({domain}, {map_name}) chain '
              f'm={len(flipped[0].starts)}..'
              f'{len(flipped[-1].starts)}')

    rows = []
    for fp in flipped:
        algo = BFSFlipMOSPP(problem=fp, is_recording=False,
                            is_timing=True)
        algo.run()
        rows.append(_row(domain, map_name, len(fp.starts),
                         None, None, None, algo))

    total = sum(r['elapsed_total'] for r in rows)
    _log.info(f'done   BFS  ({domain}, {map_name}) {len(rows)} rows '
              f'elapsed={total:.2f}s')
    return rows


def _experiment_dijkstra_flip_chain(chain: _MapChain) -> list[dict]:
    """
    ========================================================================
     Solve one map's nested k-chain with DijkstraFlipMOSPP -- MOSPP
     via the axis-swap (flip to OMSPP) + a single backward Dijkstra
     pass from the shared goal that reaches ALL k starts in one
     g-ordered sweep.

     INDEPENDENT per-k runs (NOT run()+extend), for the same reason
     as `_experiment_bfs_flip_chain`: DijkstraFlipMOSPP has no
     `extend()` -- one backward Dijkstra reaches every start, so
     each k-stage is a fresh from-scratch run. Per-row metrics stay
     apples-to-apples (cost to reach the k-th start is the same
     expanded set whether grown or restarted); only total compute
     differs. Memory is node-count |OPEN|+|CLOSED| at completion;
     `elapsed` includes the flip + re-key. Same `_row` builder.

     Returns one row per k-stage (20 rows). No BPMX / prop /
     adaptive / cache / heuristic counters (default 0).

     Precondition: undirected, NON-NEGATIVE-weight grids
     (Dijkstra-family) -- satisfied by the experiment grids.
    ========================================================================
    """
    problems = list(chain)               # ascending m, OMSPP-shaped
    domain = getattr(problems[0].grid, 'domain', '') or ''
    map_name = problems[0].grid_name
    flipped = [p.flipped() for p in problems]
    _log.info(f'start  DIJK ({domain}, {map_name}) chain '
              f'm={len(flipped[0].starts)}..'
              f'{len(flipped[-1].starts)}')

    rows = []
    for fp in flipped:
        algo = DijkstraFlipMOSPP(problem=fp, is_recording=False,
                                 is_timing=True)
        algo.run()
        rows.append(_row(domain, map_name, len(fp.starts),
                         None, None, None, algo))

    total = sum(r['elapsed_total'] for r in rows)
    _log.info(f'done   DIJK ({domain}, {map_name}) {len(rows)} rows '
              f'elapsed={total:.2f}s')
    return rows


# ── Public API ──────────────────────────────────────────────────────────────

def _run_chain_experiment(experiment,
                          path_drive_pkl_in: str,
                          path_drive_grids_in: str,
                          path_drive_csv_out: str,
                          workers: int,
                          n_maps: int | None) -> None:
    """
    ========================================================================
     Shared nested-chain runner (used by both `run_astar_inc` and
     `run_astar_rep`). One task per map; one CSV to
     `path_drive_csv_out`; one (cumulative) row per (map, k) stage.

     `experiment` is a picklable callable taking a single
     `_MapChain` and returning `list[dict]`. The Inc config rides
     into the workers via a `functools.partial`; the Rep baseline
     needs no config.

     `n_maps` slices the chain list to the first N maps (toy /
     smoke mode); None processes all. `workers` is clamped to
     `min(workers, n_tasks)`.

     Flow:
       1. Download the OMSPP problems pickle + grids pickle.
       2. Group problems into per-map chains; verify the
          nested-chain preconditions; optionally toy-slice;
          wrap each chain in a `_MapChain` and re-pickle for the
          Runner.
       3. `ProblemGrid.Runner.run` dispatches one task per chain;
          each worker attaches the chain and runs the `run()` +
          `extend()` sequence via `experiment`.
       4. Flatten the per-chain row lists; write + upload the CSV.
    ========================================================================
    """
    if n_maps is not None and n_maps < 1:
        raise ValueError(f'n_maps must be >= 1; got {n_maps}')
    drive = Drive.Factory.valdas()

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
        n_tasks = len(chain_units)
        effective_workers = max(1, min(workers, n_tasks))
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'{n_tasks} nested chains (chunksize=1)')
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


def run_astar_inc(path_drive_pkl_in: str,
                  path_drive_grids_in: str,
                  path_drive_csv_out: str,
                  rule_bpmx: str | None,
                  depth_bpmx: int | None,
                  depth_prop: int | None,
                  adaptive_h: bool = _ADAPTIVE_H,
                  carry_cache: bool = _CARRY_CACHE,
                  workers: int = 10,
                  n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run AStarIncMOSPP across every map as a NESTED k-chain
     (OMSPP problems flipped to MOSPP), for ONE config
     (`rule_bpmx`, `depth_bpmx`, `depth_prop`, `adaptive_h`,
     `carry_cache`). Validates the config (fail-fast before the
     pool spins up), then delegates the download / dispatch /
     write to `_run_chain_experiment`. The config (incl.
     `adaptive_h` / `carry_cache`) ships into the workers via a
     `functools.partial`. The caller owns the output name -- pass
     the matching `adaptive_h` / `carry_cache` to `_csv_filename`
     so the `_adapt_1` / `_cacheoff` tokens tag the CSV.
    ========================================================================
    """
    _validate_config(rule_bpmx=rule_bpmx,
                     depth_bpmx=depth_bpmx,
                     depth_prop=depth_prop)
    _log.info(f'astar_inc nested: workers={workers}, '
              f'rule_bpmx={rule_bpmx!r}, depth_bpmx={depth_bpmx!r}, '
              f'depth_prop={depth_prop!r}, adaptive_h={adaptive_h}, '
              f'carry_cache={carry_cache}')
    experiment = partial(_experiment_astar_inc_chain,
                         rule_bpmx=rule_bpmx,
                         depth_bpmx=depth_bpmx,
                         depth_prop=depth_prop,
                         adaptive_h=adaptive_h,
                         carry_cache=carry_cache)
    _run_chain_experiment(
        experiment=experiment,
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_maps=n_maps)


def run_astar_inc_prop_bpmx_depth1(path_drive_pkl_in: str,
                                   path_drive_grids_in: str,
                                   rule_bpmx: str = 'CASCADE',
                                   workers: int = 10,
                                   n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the COMBINED (prop x bpmx) quadrant the main sweep omits:
     pre-search pathmax propagation at depth 1 AND in-search BPMX at
     depth 1, in ONE AStarIncMOSPP config, across every map as a
     nested k-chain. One config-named CSV to `Results/`
     (`astar_inc_nested_rule_{rule}_bpmx_1_prop_1[_toy{N}].csv`).

     Order is fixed by the sub-search lifecycle, matching the
     "prop first, then bpmx" intuition -- and it is the ONLY order
     possible: `propagate_pathmax(1)` runs at each sub-search's init
     (pre-search), THEN the in-search BPMX(rule, depth=1) cascade
     fires during expansion. Both max-combine into the one shared
     HBounded layer, so the result is admissible -- optimality is
     preserved (verified at the unit level in AStarIncMOSPP Group D).

     Why this is not already in the sweep: `_all_inc_configs`
     deliberately ISOLATES the two axes -- the rule ladders hold
     depth_prop=0 and the prop ladder holds rule_bpmx=None -- so no
     swept config exercises both at once. This is the depth-1 x
     depth-1 corner of the missing combined quadrant.

     `rule_bpmx` selects the in-search Felner rule (default
     'CASCADE' -- the canonical bidirectional pathmax, mirroring
     the AStarIncMOSPP Group-D combined fixture). Rule '2' is also
     valid (it is structurally depth-1-only). Both depths are
     pinned to 1; vary `rule_bpmx` to compare rules at this corner.
    ========================================================================
    """
    run_astar_inc(
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=(
            f'Results/{_csv_filename(rule_bpmx, 1, 1, n_maps)}'),
        rule_bpmx=rule_bpmx,
        depth_bpmx=1,
        depth_prop=1,
        workers=workers,
        n_maps=n_maps)


def run_astar_rep(path_drive_pkl_in: str,
                  path_drive_grids_in: str,
                  path_drive_csv_out: str,
                  workers: int = 10,
                  n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the AStarRepMOSPP baseline across every map as a NESTED
     k-chain, exploiting prefix reuse: per map ONE AStarRepMOSPP
     `run()`s the smallest-k instance, then `extend()`s by each
     stage's +10 genuinely-new starts -- so each start's
     independent A* runs exactly once across the chain (no prefix
     re-solve). Single config (no rule / depth ladder); same CSV
     schema as the Inc runs. Delegates to `_run_chain_experiment`.
    ========================================================================
    """
    _log.info(f'astar_rep nested: workers={workers}')
    _run_chain_experiment(
        experiment=_experiment_astar_rep_chain,
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_maps=n_maps)


def run_astar_flip(path_drive_pkl_in: str,
                   path_drive_grids_in: str,
                   path_drive_csv_out: str,
                   workers: int = 10,
                   n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the AStarFlipMOSPP solver across every map as a NESTED
     k-chain: per map ONE AStarFlipMOSPP `run()`s the smallest-k
     instance, then `extend()`s by each stage's +10 genuinely-new
     starts. MOSPP solved by flipping to OMSPP and growing ONE
     incremental kA* search outward from the shared goal -- the
     OMSPP-side counterpart to the forward `AStarIncMOSPP`.
     Single config; same CSV schema (BPMX/prop/adapt/cache
     columns default to 0). Delegates to `_run_chain_experiment`.
    ========================================================================
    """
    _log.info(f'kastar_inc nested: workers={workers}')
    _run_chain_experiment(
        experiment=_experiment_astar_flip_chain,
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_maps=n_maps)


def run_bfs_flip(path_drive_pkl_in: str,
                 path_drive_grids_in: str,
                 path_drive_csv_out: str,
                 workers: int = 10,
                 n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the BFSFlipMOSPP solver across every map's nested k-chain
     as INDEPENDENT per-k from-scratch runs (BFS has no `extend()`;
     one backward BFS pass reaches all k starts). Single config;
     same CSV schema (BPMX/prop/adapt/cache/h columns default to 0).
     Per-row metrics are apples-to-apples with the incremental algos
     -- see `_experiment_bfs_flip_chain`. Delegates to
     `_run_chain_experiment`. Precondition: undirected, uniform-
     weight grids.
    ========================================================================
    """
    _log.info(f'bfs_flip nested: workers={workers}')
    _run_chain_experiment(
        experiment=_experiment_bfs_flip_chain,
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_maps=n_maps)


def run_dijkstra_flip(path_drive_pkl_in: str,
                      path_drive_grids_in: str,
                      path_drive_csv_out: str,
                      workers: int = 10,
                      n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the DijkstraFlipMOSPP solver across every map's nested
     k-chain as INDEPENDENT per-k from-scratch runs (Dijkstra has
     no `extend()`; one backward Dijkstra pass reaches all k
     starts). Single config; same CSV schema (BPMX/prop/adapt/cache/
     h columns default to 0). Per-row metrics are apples-to-apples
     with the incremental algos -- see
     `_experiment_dijkstra_flip_chain`. Delegates to
     `_run_chain_experiment`. Precondition: undirected, non-
     negative-weight grids.
    ========================================================================
    """
    _log.info(f'dijkstra_flip nested: workers={workers}')
    _run_chain_experiment(
        experiment=_experiment_dijkstra_flip_chain,
        path_drive_pkl_in=path_drive_pkl_in,
        path_drive_grids_in=path_drive_grids_in,
        path_drive_csv_out=path_drive_csv_out,
        workers=workers,
        n_maps=n_maps)


# ── Full INC config sweep (sequential) ──────────────────────────────────────

# Per-rule in-search BPMX depth ladders. depth_prop is held at 0
# (propagation OFF) so each ladder isolates the in-search BPMX effect.
# depth_bpmx must be >= 1, so the "depth 0" point of every ladder is BPMX
# OFF -- the rule is then irrelevant and the point collapses to the single
# shared baseline below. Rule '2' is depth-locked to 1 by AStarIncMOSPP.
_RULE_DEPTH_LADDERS: dict[str, tuple[int, ...]] = {
    '1':       (1, 2, 3, 4, 5),
    '2':       (1,),
    '3':       (1, 2, 3, 4, 5),
    'CASCADE': (1, 2, 3, 4, 5),
}

# No-BPMX pre-search pathmax propagation ladder. depth_prop == 0 is the
# shared baseline (no propagation), emitted once below, so this starts at 1.
_PROP_LADDER: tuple[int, ...] = (1, 2, 3, 4, 5)

# The single shared origin of every ladder: in-search BPMX OFF AND no
# pre-search propagation. The "depth 0" point of all five ladders decodes
# to exactly this, so it is run ONCE.
_BASELINE_CONFIG: tuple[str | None, int | None, int] = (None, None, 0)


def _all_inc_configs() -> list[tuple[str | None, int | None, int]]:
    """
    ========================================================================
     Build the full ordered list of UNIQUE INC configs for the
     sequential sweep, as (rule_bpmx, depth_bpmx, depth_prop)
     trios:

       - one shared baseline (None, None, 0) -- BPMX OFF, no
         propagation; the "depth 0" point common to every ladder,
         emitted ONCE;
       - per-rule in-search BPMX depth ladders (rules 1/3/CASCADE
         at depth_bpmx 1..5, rule 2 at depth_bpmx 1), depth_prop=0;
       - the no-BPMX pre-search propagation ladder (depth_prop 1..5).

     22 configs total. Order: baseline first, then the rule
     ladders, then the propagation ladder -- so the shared point
     runs first and a mid-sweep crash leaves the most-comparable
     CSVs already done.
    ========================================================================
    """
    configs: list[tuple[str | None, int | None, int]] = [_BASELINE_CONFIG]
    for rule, depths in _RULE_DEPTH_LADDERS.items():
        for depth_bpmx in depths:
            configs.append((rule, depth_bpmx, 0))
    for depth_prop in _PROP_LADDER:
        configs.append((None, None, depth_prop))
    return configs


def run_astar_inc_all_configs(path_drive_pkl_in: str,
                              path_drive_grids_in: str,
                              workers: int = 10,
                              n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the FULL INC config sweep IN SEQUENCE: one
     `run_astar_inc` per unique config from `_all_inc_configs`
     (22 runs), each writing its own config-named CSV under
     `Results/` (via `_csv_filename`, so runs never clobber).

     The five ladders (rule 1/2/3/CASCADE BPMX-depth, plus the
     no-BPMX propagation-depth ladder) share one origin -- BPMX
     OFF + no propagation -- so that (None, None, 0) baseline is
     run ONCE up front, not once per ladder.

     Sequential (not nested): each config is itself a full
     25-map x 20-stage run already parallel across maps, so the
     pool's cores go to ONE config at a time. `run_astar_inc`
     rebuilds the worker pool per config and validates each.

     `n_maps` toy-slices every run identically (CSVs get the
     `_toy{N}` suffix); `workers` is forwarded unchanged.
    ========================================================================
    """
    configs = _all_inc_configs()
    _log.info(f'astar_inc ALL configs: {len(configs)} sequential runs '
              f'(workers={workers}, n_maps={n_maps})')
    for i, (rule_bpmx, depth_bpmx, depth_prop) in enumerate(configs, 1):
        path_drive_csv_out = (
            f'Results/'
            f'{_csv_filename(rule_bpmx, depth_bpmx, depth_prop, n_maps)}')
        _log.info(f'[{i}/{len(configs)}] rule={rule_bpmx!r} '
                  f'depth_bpmx={depth_bpmx!r} depth_prop={depth_prop!r} '
                  f'-> {path_drive_csv_out}')
        run_astar_inc(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            depth_prop=depth_prop,
            workers=workers,
            n_maps=n_maps)
    _log.info(f'astar_inc ALL configs: {len(configs)} runs complete')


# ── Flat-pool full sweep (fastest) ──────────────────────────────────────────

def _upload_rows(drive: Drive,
                 rows: list[dict],
                 path_drive_csv_out: str) -> None:
    """
    ========================================================================
     Write `rows` to a temp CSV (header = `_CSV_COLUMNS`,
     extra keys ignored) and upload to `path_drive_csv_out` on
     Drive; always clean up the temp file.
    ========================================================================
    """
    fd_csv, path_csv = tempfile.mkstemp(suffix='.csv')
    os.close(fd_csv)
    try:
        with open(path_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=_CSV_COLUMNS,
                                    extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        drive.upload(path_src=path_csv, path_dest=path_drive_csv_out)
    finally:
        if os.path.exists(path_csv):
            os.unlink(path_csv)


class _ConfigMapChain:
    """
    ========================================================================
     Flat-pool task unit: one INC config paired with one map's
     nested k-chain.

     Wrapping (config x chain) lets the whole 22-config x 25-map
     sweep run as ONE flat pool of 550 work items, so the worker
     pool, the grids load, and the per-grid StateCell-cache build
     are paid ONCE for the entire sweep (not once per config), and
     dynamic scheduling keeps every worker saturated to the end.

     Exposes exactly what `ProblemGrid.Runner._worker_task` needs
     -- `grid_name` and `attach(grid, states)` -- by delegating to
     the wrapped `_MapChain`, plus `__iter__` so the existing
     `_experiment_astar_inc_chain` runs on it unchanged.

     The wrapped `_MapChain` instances are SHARED across the 22
     configs of a map, so one `pickle.dump` of the task list
     memoizes each chain's 20 detached problems ONCE on disk.
    ========================================================================
    """

    def __init__(self,
                 chain: _MapChain,
                 rule_bpmx: str | None,
                 depth_bpmx: int | None,
                 depth_prop: int) -> None:
        self._chain = chain
        self.rule_bpmx = rule_bpmx
        self.depth_bpmx = depth_bpmx
        self.depth_prop = depth_prop

    @property
    def grid_name(self) -> str:
        """
        ====================================================================
         Delegate to the wrapped chain (Runner reads this).
        ====================================================================
        """
        return self._chain.grid_name

    def attach(self, grid, states=None) -> None:
        """
        ====================================================================
         Delegate to the wrapped chain (Runner calls this to
         rehydrate the chain's problems onto the worker's grid).
        ====================================================================
        """
        self._chain.attach(grid=grid, states=states)

    def __iter__(self):
        """
        ====================================================================
         Iterate the wrapped chain's problems (ascending m) so
         `_experiment_astar_inc_chain` runs on this unit unchanged.
        ====================================================================
        """
        return iter(self._chain)


def _experiment_inc_flat(unit: _ConfigMapChain) -> list[dict]:
    """
    ========================================================================
     Flat-pool worker experiment: run the unit's single INC config
     on its map-chain by delegating to the shared
     `_experiment_astar_inc_chain`. Returns the chain's 20
     (cumulative) rows. Module-level => picklable for the pool.
    ========================================================================
    """
    return _experiment_astar_inc_chain(
        unit,
        rule_bpmx=unit.rule_bpmx,
        depth_bpmx=unit.depth_bpmx,
        depth_prop=unit.depth_prop)


def run_astar_inc_all_configs_flat(path_drive_pkl_in: str,
                                   path_drive_grids_in: str,
                                   workers: int = 11,
                                   n_maps: int | None = None) -> None:
    """
    ========================================================================
     Fastest full INC sweep: run all 22 configs x every map as ONE
     flat pool of (config, map-chain) tasks, then split the
     results into 22 config-named CSVs uploaded to `Results/`
     (identical names / schema to `run_astar_inc_all_configs`, so
     the s_5 report reads them unchanged).

     Why this beats the sequential driver
       `run_astar_inc_all_configs` spins a FRESH pool per config
       (22x), paying -- 22 times -- the pool spawn, the per-worker
       grids load, the per-worker StateCell-cache build over all
       grids (the dominant init cost), and the input download; and
       it eats an idle-worker TAIL as each config's uneven chains
       drain. This driver pays every fixed cost ONCE and, with
       ~550 tasks over `workers` cores (deep oversubscription),
       keeps all workers busy to the end -- makespan approaches the
       ideal total_work / workers, cheap configs filling the gaps
       expensive ones leave.

     Task ordering is map-major (every config of a map, then the
     next map) so the dispatch tail is a MIX of cheap+expensive
     configs rather than a cluster of one config -- a cheap hedge;
     with tasks ~50x the worker count the tail is at most one task
     regardless.

     Flow
       1. Download problems + grids ONCE.
       2. Per-map chains; verify nesting; optional toy-slice.
       3. Cross each surviving chain with every `_all_inc_configs`
          config -> shared-chain task units.
       4. ONE `ProblemGrid.Runner.run` over all tasks (chunksize=1,
          dynamic) -> results in submission order.
       5. Regroup results by config (results[i] <-> units[i]) and
          write + upload one CSV per config.

     `n_maps` toy-slices the map set (CSVs get `_toy{N}`).
     `workers` defaults to 11 (one shy of a 12-core box; each
     worker also holds all grids + caches in RAM -- drop it if RAM
     bites).
    ========================================================================
    """
    if n_maps is not None and n_maps < 1:
        raise ValueError(f'n_maps must be >= 1; got {n_maps}')

    configs = _all_inc_configs()
    # Fail fast on any bad config BEFORE the pool spins up.
    for rule_bpmx, depth_bpmx, depth_prop in configs:
        _validate_config(rule_bpmx=rule_bpmx,
                         depth_bpmx=depth_bpmx,
                         depth_prop=depth_prop)

    drive = Drive.Factory.valdas()
    _log.info(f'astar_inc FLAT sweep: {len(configs)} configs '
              f'(workers={workers}, n_maps={n_maps})')

    fd_in, path_in = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_in)
    fd_g, path_grids = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_g)
    fd_run, path_run = tempfile.mkstemp(suffix='.pkl')
    os.close(fd_run)

    try:
        # 1. Download inputs ONCE.
        _log.info(f'downloading {path_drive_pkl_in}')
        drive.download(path_src=path_drive_pkl_in, path_dest=path_in)
        _log.info(f'downloading {path_drive_grids_in}')
        drive.download(path_src=path_drive_grids_in, path_dest=path_grids)

        # 2. Group into per-map chains; verify nesting; toy-slice.
        with open(path_in, 'rb') as f:
            problems = pickle.load(f)
        _log.info(f'loaded {len(problems):,} problems')
        chains = _build_chains(problems)
        _verify_chains(chains)
        map_chains = [_MapChain(c) for c in chains.values()]
        if n_maps is not None:
            map_chains = map_chains[:n_maps]
            _log.info(f'toy mode: sliced to first {len(map_chains)} maps')
        _log.info(f'built {len(map_chains)} per-map chains '
                  f'(nesting verified)')

        # 3. Cross every map-chain with every config (map-major).
        #    Chains are SHARED across a map's 22 configs, so the
        #    on-disk pickle memoizes each chain's problems once.
        units: list[_ConfigMapChain] = [
            _ConfigMapChain(chain, rule_bpmx, depth_bpmx, depth_prop)
            for chain in map_chains
            for rule_bpmx, depth_bpmx, depth_prop in configs]
        with open(path_run, 'wb') as f:
            pickle.dump(units, f, protocol=pickle.HIGHEST_PROTOCOL)

        # 4. ONE pool over all (config, chain) tasks.
        n_tasks = len(units)
        effective_workers = max(1, min(workers, n_tasks))
        _log.info(f'spawning {effective_workers} workers '
                  f'(requested {workers}, n_tasks={n_tasks}); '
                  f'{len(configs)} configs x {len(map_chains)} maps '
                  f'= {n_tasks} (config, chain) tasks (chunksize=1)')
        results = ProblemGrid.Runner.run(
            path_problems=path_run,
            path_grids=path_grids,
            experiment=_experiment_inc_flat,
            workers=effective_workers,
            chunksize=1)

        # 5. Regroup by config (results[i] <-> units[i]); one CSV each.
        rows_by_cfg: dict[tuple, list[dict]] = defaultdict(list)
        for unit, chain_rows in zip(units, results):
            cfg = (unit.rule_bpmx, unit.depth_bpmx, unit.depth_prop)
            rows_by_cfg[cfg].extend(chain_rows)
        _log.info(f'received rows for {len(rows_by_cfg)} configs; '
                  f'writing + uploading {len(configs)} CSVs')
        for cfg in configs:
            rows = rows_by_cfg.get(cfg, [])
            if not rows:
                _log.warning(f'no rows for config {cfg} -- skipping CSV')
                continue
            path_drive_csv_out = f'Results/{_csv_filename(*cfg, n_maps)}'
            _upload_rows(drive=drive,
                         rows=rows,
                         path_drive_csv_out=path_drive_csv_out)
            _log.info(f'uploaded {len(rows):,} rows -> '
                      f'{path_drive_csv_out}')
        _log.info(f'astar_inc FLAT sweep: {len(configs)} CSVs complete')

    finally:
        for path in (path_in, path_grids, path_run):
            if os.path.exists(path):
                os.unlink(path)


# ── Adaptive-A* configs (depth-1; cache + adaptive on top) ──────────────────

# The four ADAPTIVE configs: every one keeps the carried on-path cache AND
# turns on Adaptive A* (`adaptive_h=True` -> the C_i-g_i CLOSED-list bound
# store accumulates ON TOP of the cache). All in-search BPMX / pre-search
# propagation depths are pinned to 1. As (rule_bpmx, depth_bpmx, depth_prop)
# trios (every one run with adaptive_h=True):
#   1. adaptive only                     (None,      None, 0)
#   2. adaptive + BPMX cascade d=1       ('CASCADE', 1,    0)
#   3. adaptive + propagation d=1        (None,      None, 1)
#   4. adaptive + cascade d=1 + prop d=1 ('CASCADE', 1,    1)
# Each writes a config-named CSV with the `_adapt_1` token, so it never
# clobbers the non-adaptive run of the same rule/depth/prop -- config 4 in
# particular is DISTINCT from the non-adaptive cascade+prop combo
# `astar_inc_nested_rule_CASCADE_bpmx_1_prop_1.csv` (run by `inc_pb`).
_ADAPTIVE_CONFIGS: list[tuple[str | None, int | None, int]] = [
    (None,      None, 0),
    ('CASCADE', 1,    0),
    (None,      None, 1),
    ('CASCADE', 1,    1),
]


def run_astar_inc_adaptive_configs(path_drive_pkl_in: str,
                                   path_drive_grids_in: str,
                                   workers: int = 10,
                                   n_maps: int | None = None) -> None:
    """
    ========================================================================
     Run the four ADAPTIVE depth-1 configs IN SEQUENCE (cache +
     Adaptive A* on top): one `run_astar_inc(adaptive_h=True)` per
     config from `_ADAPTIVE_CONFIGS`, each writing its own
     `_adapt_1`-tagged CSV under `Results/` (via `_csv_filename`,
     so they never clobber the non-adaptive runs). Mirror of
     `run_astar_inc_all_configs` with `adaptive_h=True` forced on.

     Sequential (not nested): each config is itself a full
     25-map x 20-stage run already parallel across maps, so the
     pool's cores go to ONE config at a time. `n_maps` toy-slices
     every run identically (CSVs get `_adapt_1_toy{N}`).
    ========================================================================
    """
    _log.info(f'astar_inc ADAPTIVE configs: {len(_ADAPTIVE_CONFIGS)} '
              f'sequential runs (adaptive_h=True, workers={workers}, '
              f'n_maps={n_maps})')
    for i, (rule_bpmx, depth_bpmx, depth_prop) in enumerate(
            _ADAPTIVE_CONFIGS, 1):
        csv_name = _csv_filename(rule_bpmx, depth_bpmx, depth_prop,
                                 n_maps, adaptive_h=True)
        path_drive_csv_out = f'Results/{csv_name}'
        _log.info(f'[{i}/{len(_ADAPTIVE_CONFIGS)}] rule={rule_bpmx!r} '
                  f'depth_bpmx={depth_bpmx!r} depth_prop={depth_prop!r} '
                  f'adaptive_h=True -> {path_drive_csv_out}')
        run_astar_inc(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            depth_prop=depth_prop,
            adaptive_h=True,
            workers=workers,
            n_maps=n_maps)
    _log.info(f'astar_inc ADAPTIVE configs: {len(_ADAPTIVE_CONFIGS)} '
              f'runs complete')


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # The __main__ guard is mandatory: macOS uses `spawn` for
    # ProcessPoolExecutor, so each worker re-imports this module.
    # Without the guard, every worker would re-launch the run.
    path_drive_pkl_in = 'Experiments/OMSPP/i_3_problems.pkl'
    path_drive_grids_in = 'Experiments/Grids/grids.pkl'
    # 11 = one shy of a 12-core box (leaves a core for the main
    # process); each worker also holds all grids + caches in RAM.
    workers = 11

    # Toy mode: process only the first N of the 25 maps
    # (None == all 25). Useful for smoke-testing before a full
    # run -- N=1 is one nested chain (~200 sub-searches).
    n_maps = None

    # Which algorithm to run this invocation:
    #   'inc'     -- AStarIncMOSPP, ONE BPMX config (the depth ladder
    #                is run by repeating with different rule/depth).
    #   'inc_all' -- AStarIncMOSPP, the FULL 22-config sweep as ONE
    #                FLAT pool (fastest); one CSV per config. See
    #                `run_astar_inc_all_configs_flat`. The sequential
    #                `run_astar_inc_all_configs` stays as a fallback.
    #   'inc_pb'  -- AStarIncMOSPP, the COMBINED prop-1 + bpmx-1
    #                config (the depth-1 x depth-1 corner the sweep
    #                omits). See `run_astar_inc_prop_bpmx_depth1`.
    #   'inc_adapt' -- AStarIncMOSPP, the FOUR adaptive-A* depth-1
    #                configs (cache + adaptive on top): adaptive only /
    #                +cascade d1 / +prop d1 / +cascade+prop d1. One
    #                `_adapt_1`-tagged CSV each. See
    #                `run_astar_inc_adaptive_configs`.
    #   'inc_adapt_nocache' -- AStarIncMOSPP, pure Adaptive A* (Koenig
    #                2005): ADAPT on, CACHE off (the missing cache-off
    #                cell of the 2x2 ablation -- isolates the C_i-g_i
    #                bound from the cache + its early-termination). One
    #                `_adapt_1_cacheoff`-tagged CSV (rule=None, no prop).
    #   'flip'    -- AStarFlipMOSPP: MOSPP via flip-to-OMSPP +
    #                incremental kA* (one growing search from the
    #                shared goal). Single config. See
    #                `run_astar_flip`.
    #   'bfs'     -- BFSFlipMOSPP: MOSPP via flip-to-OMSPP backward
    #                BFS (uniform-weight). INDEPENDENT per-k runs (no
    #                extend). Single config. See `run_bfs_flip`.
    #   'dijkstra'-- DijkstraFlipMOSPP: MOSPP via flip-to-OMSPP
    #                backward Dijkstra (non-negative weights).
    #                INDEPENDENT per-k runs. See `run_dijkstra_flip`.
    #   'rep'     -- AStarRepMOSPP baseline (single config, no ladder).
    ALGO = 'inc_adapt_nocache'

    if ALGO == 'inc':
        # ── AStarIncMOSPP config — one run, one config, one CSV ──────────────
        # rule_bpmx  : {None, '1', '2', '3', 'CASCADE'}; None = BPMX off.
        # depth_bpmx : int >= 1, or None = BPMX to convergence.
        # depth_prop : 0 = no propagation; int >= 1 = propagate to that
        #              depth; None = propagate to convergence.
        rule_bpmx = 'CASCADE'
        depth_bpmx = 5
        depth_prop = 0

        # Output path — encodes the config so repeated single-config
        # runs never clobber each other; `_toy{N}` suffix in toy mode.
        path_drive_csv_out = (
            f'Results/'
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

    elif ALGO == 'inc_all':
        # ── Full INC sweep — FLAT pool (fastest), one CSV per config ─────────
        # rule 1/3/CASCADE x depth_bpmx 1..5, rule 2 x depth_bpmx 1
        # (all depth_prop=0), plus the no-BPMX propagation ladder
        # depth_prop 1..5, plus the shared (None,None,0) baseline once
        # = 22 configs x every map run as ONE pool: pool spawn, grids
        # load, per-grid cache build, and download paid ONCE (not 22x),
        # dynamic scheduling busy to the end.
        run_astar_inc_all_configs_flat(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'inc_pb':
        # ── Combined prop-1 + bpmx-1 — the depth-1 x depth-1 corner ──────────
        # Pre-search propagate_pathmax(1) THEN in-search BPMX(rule, 1),
        # both max-combined into one admissible HBounded layer. The
        # sweep isolates the axes; this runs them together. Vary
        # `rule_bpmx` ('CASCADE' default; '1'/'2'/'3' also valid) to
        # compare rules at this corner.
        run_astar_inc_prop_bpmx_depth1(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            rule_bpmx='CASCADE',
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'inc_adapt':
        # ── Adaptive A* (depth-1) — 4 configs, cache + adaptive on top ───────
        # adaptive only / +cascade d1 / +prop d1 / +cascade+prop d1, all
        # with adaptive_h=True (the C_i-g_i CLOSED-list bound store added
        # on top of the carried cache). Each CSV gets the `_adapt_1` token,
        # so none clobbers a non-adaptive run (incl. the inc_pb combo).
        run_astar_inc_adaptive_configs(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'inc_adapt_nocache':
        # ── Pure Adaptive A* — ADAPT on, CACHE off (Koenig 2005) ─────────────
        # The missing cache-off cell of the 2x2 ablation: isolates the
        # C_i-g_i CLOSED-list bound store from the on-path cache (and its
        # cache-hit-at-init early-termination, which goes to 0 here). One
        # config: adaptive only, no BPMX, no propagation (rule=None,
        # depth_bpmx=None, depth_prop=0). The `_cacheoff` token keeps its
        # CSV distinct from the cache-on `inc_adapt` baseline of the same
        # rule/depth/prop. (BPMX/prop variants are omitted: BPMX needs the
        # cache as its inconsistency engine on consistent Manhattan h, so
        # they would collapse onto this config -- add them only if a harder
        # fixture motivates it.)
        rule_bpmx = None
        depth_bpmx = None
        depth_prop = 0
        path_drive_csv_out = (
            f'Results/'
            f'{_csv_filename(rule_bpmx, depth_bpmx, depth_prop, n_maps, adaptive_h=True, carry_cache=False)}')

        run_astar_inc(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            depth_prop=depth_prop,
            adaptive_h=True,
            carry_cache=False,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'rep':
        # AStarRepMOSPP baseline — single config, one CSV.
        path_drive_csv_out = (
            f'Results/{_csv_filename_rep(n_maps)}')

        run_astar_rep(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'flip':
        # AStarFlipMOSPP — MOSPP via flip-to-OMSPP incremental kA*.
        path_drive_csv_out = (
            f'Results/{_csv_filename_flip(n_maps)}')

        run_astar_flip(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'bfs':
        # BFSFlipMOSPP — MOSPP via flip-to-OMSPP backward BFS
        # (uniform-weight); independent per-k runs.
        path_drive_csv_out = (
            f'Results/{_csv_filename_bfs_flip(n_maps)}')

        run_bfs_flip(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            workers=workers,
            n_maps=n_maps)

    elif ALGO == 'dijkstra':
        # DijkstraFlipMOSPP — MOSPP via flip-to-OMSPP backward
        # Dijkstra (non-negative weights); independent per-k runs.
        path_drive_csv_out = (
            f'Results/{_csv_filename_dijkstra_flip(n_maps)}')

        run_dijkstra_flip(
            path_drive_pkl_in=path_drive_pkl_in,
            path_drive_grids_in=path_drive_grids_in,
            path_drive_csv_out=path_drive_csv_out,
            workers=workers,
            n_maps=n_maps)

    else:
        raise ValueError(
            f"ALGO must be 'inc', 'inc_all', 'inc_pb', 'inc_adapt', "
            f"'inc_adapt_nocache', 'rep', 'flip', 'bfs' or 'dijkstra'; "
            f"got {ALGO!r}")

    _log.info('--- done ---')
