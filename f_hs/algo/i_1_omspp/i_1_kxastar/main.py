from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_1_omspp._single_goal_view import _SingleGoalView
from f_hs.algo.i_1_omspp.i_0_base.main import (
    AlgoOMSPP, PHASE_SEARCH,
)
from f_hs.algo.i_1_omspp.mixins.extendable import ExtendableOMSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KxAStarOMSPP(Generic[State],
              AlgoOMSPP[State],
              ExtendableOMSPP[State]):
    """
    ============================================================================
     Repetitive k×A* (kxA*_min) for the One-to-Many Shortest
     Path Problem — the OMSPP **paper baseline**.

     Runs `k` INDEPENDENT A* sub-searches, one per goal, with
     NO state sharing across sub-searches. Each sub-search
     builds its own `SearchStateSPP` from scratch, expands its
     own subset of the graph, and returns a `SolutionSPP`. The
     orchestrator aggregates per-goal results into a
     `SolutionOMSPP` Mapping.

     Used as the **comparison baseline** for state-sharing
     OMSPP algorithms (`KAStarInc`, `KAStarAgg`, `KBFS`,
     `KDijkstra`): k×A* expands each goal's search tree
     independently, so cumulative `cnt_expanded` /
     `cnt_generated` is the upper bound that state-sharing
     algos aim to beat.

     Per Stern et al. (OMSPP/MOSPP submission), this is the
     `kA*_min`/`kA*_rep` algorithm — k repetitions of the
     base A*, no inter-search reuse.

     **Assumptions / requirements:**

       - **Admissible heuristic** (consistency is NOT required —
         unlike `KAStarInc`, k×A* has no fast-path that relies
         on consistency).
       - Edge costs non-negative (inherited from `ProblemSPP`
         / A* correctness conditions).

     **Composes the `ExtendableOMSPP` capability mixin**, but
     gets only a SUBSET of the mixin's value compared to
     `KAStarInc`:

       Provided by the mixin and useful here:
         - `extend(new_goals)` — append goals, run A* on each
           genuinely-new goal only. The fast-path
           `goal in self._solutions` (`reason='already_reached'`)
           skips A* entirely on duplicates and on goals
           re-submitted across `extend()` calls.
         - `run_nested(problems, h, ...)` — classmethod
           convenience for prefix-extending problem sequences.
         - Cumulative counters / elapsed / recorder semantics.

       Provided by the mixin but **structurally inert** here:
         - Lazy re-push of the trailing reached goal — k×A*
           has no shared frontier; `_repush_last_reached_goal`
           is a no-op.
         - Already-closed fast-path — k×A* has no shared
           CLOSED set; the branch never fires.
         - PHASE_UPDATE / refresh_priorities transition — no
           shared frontier to refresh.

     Recording schema (subset of the canonical OMSPP 5-event
     set):
       - `push`, `pop`, `decrease_g` — emitted by each inner
         AStar via the shared recorder.
       - `on_goal` — per goal, with `reason ∈ {expanded,
         already_reached, unreachable}`. The
         `already_closed` reason is never emitted (no shared
         CLOSED set).
       - `update_frontier` — **NOT emitted** (no
         between-sub-search frontier transition). Analogous
         to AGG-lazy, which also doesn't emit
         `update_frontier`.
    ============================================================================
    """

    # Counter scaffold: drops `cnt_h_update` (kxA* has no
    # between-sub-search refresh phase). Honest API surface
    # per the per-class counter convention.
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search',),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'KxAStarOMSPP',
                 is_recording: bool = False,
                 is_timing: bool = True,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `h` is a bi-arg callable `h(state, goal) -> int`. Each
         sub-search closes over its goal via the standard
         default-arg idiom (no late-binding pitfall) and wraps
         with a counter that routes every call to
         `cnt_h_search`. There is no `cnt_h_update` — kxA* has
         no between-sub-search refresh, so the structural
         UPDATE phase is never entered.

         Only `is_timing=True` is meaningful in the limited
         sense that `elapsed_search` accumulates per
         sub-search wall-clock; `elapsed_update` stays at 0.0
         by design (no UPDATE flips).
        ====================================================================
        """
        AlgoOMSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        # ExtendableOMSPP bookkeeping — full goal sequence
        # seen so far (across run + every extend), and the
        # trailing reached goal. _last_algo is tracked for
        # contract symmetry with KAStarInc but is never
        # consulted by _repush_last_reached_goal (no shared
        # state to push into).
        self._all_goals: list[State] = []
        self._last_reached_goal: State | None = None
        self._last_algo: AStar[State] | None = None
        # Peak memory across sub-searches — k×A* discards
        # each sub-search's bundle, so the default
        # _sync_memory_snapshot probe finds nothing. Track
        # peak (open, closed) memory inline as sub-searches
        # complete; expose via the overridden
        # `_sync_memory_snapshot`.
        self._mem_open_peak: int = 0
        self._mem_closed_peak: int = 0

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Run k independent A* sub-searches sequentially.
         Delegates the per-goal loop body to `_handle_goal`,
         shared with the `ExtendableOMSPP` mixin's `extend()`.
        ====================================================================
        """
        self._all_goals = list(self.problem.goals)
        self._last_reached_goal = None
        self._last_algo = None
        self._mem_open_peak = 0
        self._mem_closed_peak = 0
        for i, goal in enumerate(self._all_goals):
            self._handle_goal(goal, idx=i)
        return SolutionOMSPP(self._solutions)

    def _handle_goal(self, goal: State, idx: int) -> None:
        """
        ====================================================================
         Per-goal sub-search body. Shared by `_run()` and
         `ExtendableOMSPP.extend()`.

         Skips A* on the `already_reached` fast-path when a
         prior sub-search (within this run, or any prior
         `extend()`) already finalized `goal`'s cost. This is
         the sole efficiency the mixin contributes to k×A*.
        ====================================================================
        """
        # Fast-path: already solved by a prior sub-search. The
        # `already_closed` branch is omitted entirely — k×A*
        # has no shared CLOSED set.
        if goal in self._solutions:
            sol = self._solutions[goal]
            self._emit_on_goal(goal, cost=sol.cost,
                               reason='already_reached',
                               goal_index=idx)
            return

        # Build sub-problem (single-goal view) and a FRESH
        # AStar instance. No `search_state=...` parameter —
        # each sub-search owns its own bundle.
        sub_problem = _SingleGoalView[State](
            base=self.problem, goal=goal)
        h_i = self._make_h_for(goal)
        algo = AStar[State](
            problem=sub_problem,
            h=h_i,
            name=f'{self.name}[{idx}]',
            is_recording=False,
        )
        # Share the recorder so push/pop/decrease_g events
        # from each sub-search land in the orchestrator's
        # event stream.
        algo._recorder = self._recorder
        # Phase stays SEARCH throughout (no UPDATE flips in
        # kxA*). The explicit assignment is a no-op when
        # already SEARCH; included for contract clarity.
        self.phase = PHASE_SEARCH
        sol = algo.run()

        # Accumulate the inner sub-search's search-semantic
        # counters AND its frontier-owned heap-op counters.
        # Each sub-search has its OWN frontier — there is no
        # end-of-run sync from a shared frontier, so we
        # aggregate per-iteration here.
        ic = algo.counters
        self._counters.inc(
            'cnt_expanded', n=ic['cnt_expanded'])
        self._counters.inc(
            'cnt_generated', n=ic['cnt_generated'])
        self._counters.inc(
            'cnt_push', n=ic['cnt_push'])
        self._counters.inc(
            'cnt_pop', n=ic['cnt_pop'])
        self._counters.inc(
            'cnt_decrease', n=ic['cnt_decrease'])

        # Track peak memory across sub-searches via direct
        # introspection of this sub-search's terminal
        # SearchStateSPP. The base's _sync_memory_snapshot
        # has no shared bundle to probe, so we maintain the
        # running peak here.
        open_mem, closed_mem = self._mem_of(algo)
        if open_mem > self._mem_open_peak:
            self._mem_open_peak = open_mem
        if closed_mem > self._mem_closed_peak:
            self._mem_closed_peak = closed_mem

        # Emit on_goal.
        reason = ('expanded' if sol.cost != float('inf')
                  else 'unreachable')
        self._emit_on_goal(goal, cost=sol.cost,
                           reason=reason, goal_index=idx)
        self._solutions[goal] = sol

        # ExtendableOMSPP bookkeeping. Track only fresh
        # expansions — fast-path returns earlier and leaves
        # _last_reached_goal pointing at the prior fresh
        # expansion. _last_algo is stored for contract
        # symmetry; _repush_last_reached_goal does not
        # actually call it.
        if reason == 'expanded':
            self._last_reached_goal = goal
            self._last_algo = algo
        else:
            self._last_reached_goal = None
            self._last_algo = None

    def _repush_last_reached_goal(self) -> None:
        """
        ====================================================================
         No-op for k×A*. There is no shared frontier to
         re-push into — each sub-search builds and discards
         its own SearchStateSPP. Clearing the bookkeeping for
         hygiene; the contract requires the method to exist
         on every `ExtendableOMSPP` subclass.
        ====================================================================
        """
        self._last_reached_goal = None
        self._last_algo = None

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         No-op. k×A* has no shared frontier; heap-op counters
         are accumulated inline in `_handle_goal` per
         sub-search. Override exists to suppress the default
         hook (which would also be a no-op, but explicit is
         better than relying on inherited behavior here).
        ====================================================================
        """
        pass

    def _sync_memory_snapshot(self) -> None:
        """
        ====================================================================
         Write the tracked peak memory (open, closed) across
         sub-searches into `self._counters`. Overrides the
         base's auto-probe — kxA* has no persistent state
         bundle to inspect at end-of-run, but tracked peak
         from each sub-search gives a fair benchmark figure.
        ====================================================================
        """
        self._counters.assign('mem_open', self._mem_open_peak)
        self._counters.assign(
            'mem_closed', self._mem_closed_peak)

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, goal: State) -> list[State]:
        """
        ====================================================================
         k×A* discards each sub-search's parent pointers after
         the sub-search completes (no persistent state). Path
         reconstruction is not supported — returns `[]`.

         If a caller needs per-goal paths, hold onto each
         sub-search by capturing it from a custom subclass
         hook, or use `KAStarInc` (which retains the shared
         bundle).
        ====================================================================
        """
        return []

    # ──────────────────────────────────────────────────
    #  Internal
    # ──────────────────────────────────────────────────

    def _make_h_for(
            self, goal: State
            ) -> Callable[[State], int]:
        """
        ====================================================================
         Close over the current goal AND wrap with a counter
         — every h-call routes to `cnt_h_search`. kxA* has no
         UPDATE phase, so `cnt_h_update` does not exist in
         this algo's scaffold.
        ====================================================================
        """
        h_outer = self._h
        counters = self._counters

        def h_wrapped(s: State, g: State = goal) -> int:
            v = h_outer(s, g)
            counters.inc('cnt_h_search')
            return v

        return h_wrapped

    def _emit_on_goal(self,
                      goal: State,
                      cost: float,
                      reason: str,
                      goal_index: int,
                      ) -> None:
        """
        ====================================================================
         Emit an `on_goal` event. Carries the goal index so
         duplicate goals in `problem.goals` remain
         distinguishable.
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        self._recorder.record(dict(
            type='on_goal',
            state=goal,
            g=(int(cost) if cost != float('inf') else cost),
            reason=reason,
            goal_index=goal_index,
        ))

    def _mem_of(self,
                algo: 'AStar[State]'
                ) -> tuple[int, int]:
        """
        ====================================================================
         Compute (open, closed) memory footprint for a
         completed sub-search's `SearchStateSPP`. Mirrors the
         per-entry split logic in
         `AlgoOMSPP._sync_memory_snapshot` so the cross-algo
         memory metric is comparable.
        ====================================================================
        """
        import sys
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
