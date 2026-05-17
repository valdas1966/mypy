import random
import sys

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
from f_hs.algo.i_1_mospp._single_start_view import _SingleStartView
from f_hs.algo.i_1_mospp.i_0_base.main import (
    AlgoMOSPP, PHASE_SEARCH,
)
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)

# Deterministic seed for `order_starts='random'` so the
# sub-search order (and therefore every counter / event pin)
# is reproducible across runs.
_RANDOM_SEED = 0

_ORDER_POLICIES = ('near', 'far', 'mean', 'random')


class AStarIncMOSPP(Generic[State], AlgoMOSPP[State]):
    """
    ============================================================================
     Incremental k×A* (kA*_inc) for the Many-to-One Shortest
     Path Problem.

     Runs `k` sequential forward A* sub-searches, one per
     start, toward the **shared fixed goal**. Unlike
     `AStarRepMOSPP` (the no-sharing baseline), each sub-search
     **carries forward** what earlier sub-searches discovered
     — but NOT via a shared `SearchStateSPP` (the start varies,
     so OPEN/CLOSED/g/parent do not transfer). Instead two
     **goal-anchored** stores are accumulated and replayed:

       - **on-path cache** `cache[x] = h*(x, goal)` harvested
         by `AStarLookup.to_cache()` after each reached
         sub-search. Goal is fixed ⇒ every entry stays exact
         for later sub-searches.
       - **admissible bounds** `bounds[x] ≥ h*(x, goal)` —
         from the just-finished search's CLOSED set (SPI:
         `C_i − g_i(x)`) and from the inner `HBounded` layer
         (BPMX-lifted / pathmax-propagated values).

     **Headline win — cache-hit-at-init.** If a later start
     `s_j` is already in the carried cache, the inner
     `AStarLookup` pops it on the very first iteration and
     `_early_exit` terminates the sub-search in ONE pop, zero
     expansions, with cost `g(s_j) + h*(s_j) = h*(s_j, goal)`.

     This is a mirror of `AStarRepMOSPP._handle_start` with two
     diffs: the cache-hit-at-init accounting and the
     `to_cache` / `_harvest_bounds` reuse plumbing. The inner
     sub-search algorithm is `AStarBPMX` (which subsumes
     `AStarLookup`; `rule_bpmx=None` ⇒ behaves exactly as
     `AStarLookup`), so cache, bounds, pre-search
     `propagate_pathmax`, and in-search BPMX are all available
     through one inner class.

     **Reuse knobs** (all opt-in; defaults give the strongest
     incremental behaviour except BPMX which defaults off):

       | knob | effect |
       |---|---|
       | `carry_cache` | replay `to_cache()` harvest across sub-searches (drives cache-hit-at-init) |
       | `carry_bounds` | replay SPI + HBounded bounds across sub-searches |
       | `propagate` / `propagate_depth` | run pre-search `propagate_pathmax(depth)` per sub-search (needs seeds: cache or bounds) |
       | `rule_bpmx` / `depth_bpmx` | in-search Felner BPMX on every sub-search |

     `propagate` is a **separate boolean** from
     `propagate_depth`: `propagate_pathmax(depth=None)` means
     "run to convergence", which is distinct from "do not
     propagate at all". Without the boolean, the
     cache-only config and the propagate-to-convergence config
     would be indistinguishable.

     **Assumptions / requirements:**

       - **Admissible heuristic.** The carried cache holds
         exact h* (admissible by definition); SPI / HBounded
         entries are admissible lower bounds. Consistency is
         NOT required (BPMX exists precisely for inconsistent
         h).
       - Non-negative edge costs (inherited from `ProblemSPP`
         / A* correctness).

     Recording schema (mirrors `AStarRepMOSPP`'s subset plus
     one event):

       - `push`, `pop`, `decrease_g` — emitted by each inner
         `AStarBPMX` via the shared recorder. With the lookup
         layers active, `push` / `pop` may carry `is_cached`
         / `is_bounded` flags; pre-search `propagate_pathmax`
         emits `propagate_wave` / `propagate`; in-search BPMX
         emits its own event family.
       - `cache_hit_at_init` — emitted when a sub-search
         terminates on its very first pop via the carried
         cache. Payload: `state=start, g=cost, start_index`.
       - `on_start` — per start at sub-search end. Payload:
         `state=start, g=cost, reason ∈ {expanded,
         already_reached, unreachable}, start_index`.
       - `update_frontier` — NOT emitted (no shared frontier
         to transition).
    ============================================================================
    """

    # Counter scaffold = AStarRepMOSPP's set, widened with the
    # inner AStarBPMX propagate / bpmx groups (accumulated per
    # sub-search) and the orchestrator-owned
    # `cnt_cache_hits_at_init`.
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search',),
        ('cnt_prop_waves', 'cnt_prop_attempts', 'cnt_prop_lifts'),
        ('cnt_bpmx_attempts', 'cnt_bpmx_successes',
         'cnt_bpmx_depth'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('cnt_cache_hits_at_init',),
        ('mem_open', 'mem_closed'),
    )

    # Inner AStarBPMX counter names SUMMED per sub-search.
    # Two inner counters are deliberately excluded:
    #  - `cnt_h_search` — incremented directly on the
    #    orchestrator by the wrapped h (no inner counter).
    #  - `cnt_prop_waves` — aggregated by MAX, not SUM (see
    #    `_prop_waves_peak`): it is a propagation-DEPTH horizon
    #    ("deepest wave any sub-search ran"), not wave-work.
    #    Wave-work is already carried by the summed
    #    `cnt_prop_attempts` / `cnt_prop_lifts`. Mirrors the
    #    peak aggregation of `mem_open` / `mem_closed`.
    _INNER_COUNTER_NAMES: tuple[str, ...] = (
        'cnt_prop_attempts', 'cnt_prop_lifts',
        'cnt_bpmx_attempts', 'cnt_bpmx_successes',
        'cnt_bpmx_depth',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'AStarIncMOSPP',
                 is_recording: bool = False,
                 is_timing: bool = True,
                 order_starts: str = 'near',
                 carry_cache: bool = True,
                 carry_bounds: bool = True,
                 propagate: bool = False,
                 propagate_depth: int | None = None,
                 rule_bpmx: str | None = None,
                 depth_bpmx: int | None = 1,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `h` is a bi-arg callable `h(state, goal) -> int`. The
         goal is FIXED (MOSPP has a single goal), so the
         counter-wrapped unary h is built ONCE — closed over
         `self._goal = problem.goals[0]` — and reused across
         every sub-search (and as the ordering metric).

         `order_starts ∈ {near, far, mean, random}`:
           - `near` / `far` — ascending / descending by
             `h(start, goal)`.
           - `mean`  — ascending by `|h(start, goal) − mean|`
             (closest-to-average first).
           - `random` — deterministic shuffle (fixed seed).

         `propagate` toggles the per-sub-search pre-search
         `propagate_pathmax(depth=propagate_depth)` call;
         `propagate_depth=None` then means "to convergence".

         No `cnt_h_update` counter (no PHASE_UPDATE);
         `elapsed_update` stays 0.0 by design.
        ====================================================================
        """
        if len(problem.goals) != 1:
            raise ValueError(
                f'AStarIncMOSPP requires exactly 1 goal '
                f'(got {len(problem.goals)})')
        if order_starts not in _ORDER_POLICIES:
            raise ValueError(
                f'order_starts must be one of {_ORDER_POLICIES}; '
                f'got {order_starts!r}')
        AlgoMOSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        # The fixed goal — captured once for the closures.
        self._goal: State = problem.goals[0]
        self._order_starts: str = order_starts
        self._carry_cache: bool = carry_cache
        self._carry_bounds: bool = carry_bounds
        self._propagate: bool = propagate
        self._propagate_depth: int | None = propagate_depth
        self._rule_bpmx: str | None = rule_bpmx
        self._depth_bpmx: int | None = depth_bpmx
        # Counter-wrapped unary h, built once and reused. The
        # closure increments the ORCHESTRATOR's `cnt_h_search`
        # (the inner AStarBPMX scaffold has no such counter).
        self._h_wrapped: Callable[[State], int] = (
            self._make_h_wrapped())
        # Goal-anchored reuse stores, accumulated across
        # sub-searches.
        self._cache: dict[State, CacheEntry[State]] = {}
        self._bounds: dict[State, float] = {}
        # Peak memory across sub-searches.
        self._mem_open_peak: int = 0
        self._mem_closed_peak: int = 0
        # MAX-aggregated propagation depth: the deepest wave
        # ladder any single sub-search ran (NOT the sum). 0
        # when no sub-search propagated (empty seeds).
        self._prop_waves_peak: int = 0

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionMOSPP:
        """
        ====================================================================
         Run k sequential A* sub-searches, one per start, in
         the policy-ordered start sequence. Goal-anchored
         cache / bounds are reset here so a re-`run()` starts
         clean.
        ====================================================================
        """
        self._cache = {}
        self._bounds = {}
        self._mem_open_peak = 0
        self._mem_closed_peak = 0
        self._prop_waves_peak = 0
        ordered = self._apply_order_starts(list(self.problem.starts))
        for i, start in enumerate(ordered):
            self._handle_start(start, idx=i)
        return SolutionMOSPP(self._solutions)

    def _handle_start(self, start: State, idx: int) -> None:
        """
        ====================================================================
         Per-start sub-search body.

         Skips A* on the `already_reached` fast-path when a
         prior sub-search already finalized this start's cost
         (duplicate start). Otherwise runs a FRESH
         `AStarBPMX` over a single-start view, seeded with the
         carried cache / bounds, then harvests the result back
         into the reuse stores.
        ====================================================================
        """
        # Fast-path: already solved by a prior (duplicate)
        # start. No shared CLOSED set here, so the
        # `already_closed` reason never applies.
        if start in self._solutions:
            sol = self._solutions[start]
            self._emit_on_start(start, cost=sol.cost,
                                reason='already_reached',
                                start_index=idx)
            return

        sub_problem = _SingleStartView[State](
            base=self.problem, start=start)

        # Cache / bounds arguments. `cache` requires `goal`;
        # `goal` is harmless when `cache` is None. A bounds
        # layer must exist whenever propagation is requested
        # (its storage) — AStarBPMX auto-wraps an empty
        # bounds for BPMX, but not for propagate-only.
        cache_arg = (dict(self._cache)
                     if self._carry_cache else None)
        if self._carry_bounds:
            bounds_arg: dict[State, float] | None = dict(
                self._bounds)
        elif self._propagate:
            bounds_arg = {}
        else:
            bounds_arg = None

        # Will the inner search cache-hit on its first pop?
        hit_at_init_expected = (self._carry_cache
                                and start in self._cache)

        algo = AStarBPMX[State](
            problem=sub_problem,
            h=self._h_wrapped,
            name=f'{self.name}[{idx}]',
            is_recording=False,
            cache=cache_arg,
            goal=self._goal,
            bounds=bounds_arg,
            rule_bpmx=self._rule_bpmx,
            depth_bpmx=self._depth_bpmx,
        )
        # Share the recorder so push/pop/propagate/bpmx events
        # from each sub-search land in the orchestrator stream.
        algo._recorder = self._recorder
        self.phase = PHASE_SEARCH

        # Opt-in pre-search pathmax propagation. Seeds are the
        # cache keys + bounds keys; on the first sub-search
        # (empty cache, empty bounds) this is a no-op.
        if self._propagate:
            algo.propagate_pathmax(depth=self._propagate_depth)

        sol = algo.run()

        # Accumulate the inner sub-search's counters. Each
        # AStarBPMX owns its own scaffold; cumulative totals
        # across all sub-searches give the INC-run total.
        ic = algo.counters
        for cn in self._INNER_COUNTER_NAMES:
            self._counters.inc(cn, n=ic[cn])

        # `cnt_prop_waves` aggregates by MAX, not SUM: track the
        # deepest wave ladder any single sub-search ran (mirror
        # of the mem-peak tracking below). Flushed once in
        # `_sync_memory_snapshot`. SS1 typically contributes 0
        # (empty carried cache ⇒ no propagate seeds).
        if ic['cnt_prop_waves'] > self._prop_waves_peak:
            self._prop_waves_peak = ic['cnt_prop_waves']

        # Cache-hit-at-init: terminated on the FIRST pop via
        # the carried cache (1 pop, 0 expansions, the cache
        # hit is the start itself).
        ss = algo.search_state
        if (hit_at_init_expected
                and ss is not None
                and ss.cache_hit is not None
                and ss.cache_hit == start
                and ic['cnt_pop'] == 1
                and ic['cnt_expanded'] == 0):
            self._counters.inc('cnt_cache_hits_at_init')
            self._emit_cache_hit_at_init(
                start, cost=sol.cost, start_index=idx)

        # Track peak memory.
        open_mem, closed_mem = self._mem_of(algo)
        if open_mem > self._mem_open_peak:
            self._mem_open_peak = open_mem
        if closed_mem > self._mem_closed_peak:
            self._mem_closed_peak = closed_mem

        reason = ('expanded' if sol.cost != float('inf')
                  else 'unreachable')
        self._emit_on_start(start, cost=sol.cost,
                            reason=reason, start_index=idx)
        self._solutions[start] = sol

        # Harvest reuse stores for later sub-searches (only
        # from a reached search — to_cache / SPI need a
        # terminal).
        if sol.cost != float('inf'):
            if self._carry_cache:
                self._cache.update(algo.to_cache())
            if self._carry_bounds:
                self._harvest_bounds(algo, cost=sol.cost)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         No-op. Each sub-search owns its own frontier; heap-op
         counters are accumulated inline in `_handle_start`.
        ====================================================================
        """
        pass

    def _sync_memory_snapshot(self) -> None:
        """
        ====================================================================
         Write tracked peak / MAX-aggregated counters across
         sub-searches into `self._counters`. Overrides the
         base auto-probe (there is no single shared
         search-state to probe). Covers `mem_open` /
         `mem_closed` (peak) and `cnt_prop_waves` (deepest
         single-sub-search propagation-wave ladder — MAX, not
         SUM; the summed wave-work lives in
         `cnt_prop_attempts` / `cnt_prop_lifts`).
        ====================================================================
        """
        self._counters.assign('mem_open', self._mem_open_peak)
        self._counters.assign(
            'mem_closed', self._mem_closed_peak)
        self._counters.assign(
            'cnt_prop_waves', self._prop_waves_peak)

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, start: State) -> list[State]:
        """
        ====================================================================
         Each sub-search's parent pointers are discarded after
         the sub-search completes (no persistent shared state).
         Path reconstruction is not supported — returns `[]`
         (mirror of `AStarRepMOSPP`).
        ====================================================================
        """
        return []

    # ──────────────────────────────────────────────────
    #  Internal
    # ──────────────────────────────────────────────────

    def _apply_order_starts(self,
                            starts: list[State]
                            ) -> list[State]:
        """
        ====================================================================
         Order the start sequence per the `order_starts`
         policy, using `h(start, goal)` as the distance metric
         (the raw bi-arg h — NOT counted as search work).
         Sorts are stable, so duplicate-metric ties keep the
         original `problem.starts` order; `random` uses a
         fixed seed — every policy is deterministic.
        ====================================================================
        """
        h = self._h
        goal = self._goal
        if self._order_starts == 'random':
            out = list(starts)
            random.Random(_RANDOM_SEED).shuffle(out)
            return out
        dist = {s: h(s, goal) for s in starts}
        if self._order_starts == 'near':
            return sorted(starts, key=lambda s: dist[s])
        if self._order_starts == 'far':
            return sorted(starts, key=lambda s: -dist[s])
        # 'mean' — closest-to-average distance first.
        mean = (sum(dist.values()) / len(dist)) if dist else 0.0
        return sorted(starts, key=lambda s: abs(dist[s] - mean))

    def _harvest_bounds(self,
                        algo: 'AStarBPMX[State]',
                        cost: float) -> None:
        """
        ====================================================================
         Accumulate admissible lower bounds on h*(x, goal)
         from the just-finished sub-search (goal is fixed, so
         every bound stays valid for later sub-searches):

           - **SPI** — for every CLOSED state x:
             `h*(x, goal) ≥ C_i − g_i(x)` (the s_i→goal path
             constrained through x costs ≥ C_i; g_i(x) ≥
             g*(s_i, x), so the bound is admissible even under
             inconsistent h / suboptimal closed g).
           - **HBounded** — the inner heuristic chain's
             bounds dict (BPMX-lifted + pathmax-propagated
             admissible values).

         Cumulative max keeps the tightest bound seen.
        ====================================================================
        """
        ss = algo.search_state
        if ss is not None:
            for x in ss.closed:
                gx = ss.g.get(x)
                if gx is None:
                    continue
                cand = cost - gx
                if cand > self._bounds.get(x, float('-inf')):
                    self._bounds[x] = cand
        # Walk the heuristic chain for an HBounded storage
        # layer (BPMX / pathmax lifts live there).
        cur = algo._h
        while cur is not None:
            if isinstance(cur, HBounded):
                for k, v in cur.bounds.items():
                    if v > self._bounds.get(k, float('-inf')):
                        self._bounds[k] = v
                break
            cur = getattr(cur, '_base', None)

    def _make_h_wrapped(self) -> Callable[[State], int]:
        """
        ====================================================================
         Build the counter-wrapped unary h. Closes over the
         fixed `self._goal` and `self._counters` once; every
         call increments the orchestrator's `cnt_h_search`
         and returns `h(state, goal)`.
        ====================================================================
        """
        h_outer = self._h
        goal = self._goal
        counters = self._counters

        def h_wrapped(s: State) -> int:
            v = h_outer(s, goal)
            counters.inc('cnt_h_search')
            return v

        return h_wrapped

    def _emit_on_start(self,
                       start: State,
                       cost: float,
                       reason: str,
                       start_index: int,
                       ) -> None:
        """
        ====================================================================
         Emit an `on_start` event. Carries the start index so
         duplicate starts in `problem.starts` remain
         distinguishable (mirror of `AStarRepMOSPP`).
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        self._recorder.record(dict(
            type='on_start',
            state=start,
            g=(int(cost) if cost != float('inf') else cost),
            reason=reason,
            start_index=start_index,
        ))

    def _emit_cache_hit_at_init(self,
                                start: State,
                                cost: float,
                                start_index: int,
                                ) -> None:
        """
        ====================================================================
         Emit a `cache_hit_at_init` event — the sub-search
         terminated on its first pop via the carried cache.
         Precedes the sub-search's `on_start` marker.
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        self._recorder.record(dict(
            type='cache_hit_at_init',
            state=start,
            g=(int(cost) if cost != float('inf') else cost),
            start_index=start_index,
        ))

    def _mem_of(self,
                algo: 'AStarBPMX[State]'
                ) -> tuple[int, int]:
        """
        ====================================================================
         Compute (open, closed) memory footprint for a
         completed sub-search's `SearchStateSPP`. Mirrors
         `AStarRepMOSPP._mem_of` so the cross-algo memory
         metric is comparable.
        ====================================================================
        """
        ss = algo.search_state
        if ss is None or not hasattr(ss, 'frontier'):
            return (0, 0)
        frontier = ss.frontier
        closed = ss.closed
        g, parent = ss.g, ss.parent
        queue = getattr(frontier, '_queue', None)
        if queue is not None and hasattr(queue, '_heap'):
            frontier_struct = (sys.getsizeof(queue._heap)
                               + sys.getsizeof(queue._index)
                               + sum(sys.getsizeof(t)
                                     for t in queue._heap))
        else:
            frontier_struct = sys.getsizeof(
                queue if queue is not None else frontier)
        n_g = len(g)
        n_open = len(frontier)
        if n_g > 0:
            g_parent_total = (sys.getsizeof(g)
                              + sum(sys.getsizeof(v)
                                    for v in g.values())
                              + sys.getsizeof(parent))
            per_entry = g_parent_total / n_g
            g_parent_open = round(per_entry * n_open)
            g_parent_closed = round(per_entry * (n_g - n_open))
        else:
            g_parent_open = 0
            g_parent_closed = 0
        return (
            frontier_struct + g_parent_open,
            sys.getsizeof(closed) + g_parent_closed,
        )
