from f_hs.algo.i_0_oospp.i_1_bfs import BFS
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_omspp.i_0_base.main import AlgoOMSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class _MultiGoalBFS(Generic[State], BFS[State]):
    """
    ============================================================================
     Inner BFS specialization for KBFS: single-pass multi-goal
     search.

     Overrides:
       - `_is_goal` returns always False — KBFS controls
         termination through `_early_exit` instead.
       - `_early_exit(state)` checks whether the just-popped
         state is in the remaining goal set; if so, fires the
         orchestrator callback (which records the solution and
         emits `on_goal`) and removes it from the set. When the
         set drains to empty, returns a `SolutionSPP` to
         terminate the inner loop.

     The pattern lets the OMSPP orchestrator drive ONE BFS pass
     that observes every goal-pop in true discovery order, with
     no per-goal sub-search restarts and no force-expand.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 remaining: set[State],
                 on_goal_pop: Callable[[State, float], None],
                 name: str = 'KBFS[inner]',
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.

         `remaining` and `on_goal_pop` are mutable handles owned
         by the orchestrator: the inner consults `remaining` and
         calls `on_goal_pop(state, cost)` when a goal is popped.
        ====================================================================
        """
        BFS.__init__(self, problem=problem, name=name,
                     is_recording=is_recording)
        self._remaining: set[State] = remaining
        self._on_goal_pop: Callable[[State, float], None] = on_goal_pop

    def _is_goal(self, state: State) -> bool:
        """
        ====================================================================
         Always False — termination is fully delegated to
         `_early_exit` so the inner BFS does not stop on the
         first goal-pop.
        ====================================================================
        """
        return False

    def _early_exit(self, state: State) -> SolutionSPP | None:
        """
        ====================================================================
         Multi-goal observer: if the popped `state` is one of
         the remaining goals, fire the orchestrator callback
         and remove from the remaining set. Terminate when the
         set is empty.

         The cost reported to the callback is `g[state]` at pop
         time — guaranteed optimal for BFS on uniform-cost
         graphs (BFS layer order ≡ shortest-path distance from
         start).
        ====================================================================
        """
        if state in self._remaining:
            cost = self._search.g[state]
            self._on_goal_pop(state, cost)
            self._remaining.discard(state)
            if not self._remaining:
                return SolutionSPP(cost=cost)
        return None


class KBFS(Generic[State], AlgoOMSPP[State]):
    """
    ============================================================================
     k-BFS for the One-to-Many Shortest Path Problem on
     uniform-weight graphs.

     Runs a SINGLE BFS pass from the shared start, observing
     each goal at the moment it is popped — no per-goal sub-
     searches, no force-expand, no already-closed fast-path.
     Independent of `KAStarInc` (its own frame, sibling under
     `AlgoOMSPP`).

     Termination
       The inner `_MultiGoalBFS` neutralizes the standard
       goal-pop check (`_is_goal` always returns False) and
       routes goal detection through `_early_exit`. The pass
       terminates as soon as the last unfound goal is popped.

     Discovery order
       `on_goal` events are emitted in BFS layer order — the
       genuine order in which goals are reached from the
       shared start. `goal_index` carries the goal's position
       in `problem.goals` (input order), preserving identity
       for duplicates.

     Correctness preconditions
       Uniform edge weights (BFS depth = optimal cost). For
       non-uniform non-negative weights, use KDijkstra.

     Counters (subset of the AlgoOMSPP 8-counter scaffold):
       cnt_push / cnt_pop — frontier-sourced (FrontierFIFO).
       cnt_decrease       — always 0 (FIFO has no decrease op;
                            synthesized at the algo level).
       cnt_h_*            — always 0 (no heuristic).
       cnt_phi_*          — always 0 (no Φ aggregation).
       cnt_pop_stale      — always 0 (no lazy stale-pop).

     Within/between elapsed split
       Phase stays in `PHASE_SEARCH` for the whole run —
       `elapsed_update == 0.0` by construction. There is no
       inter-sub-search work to time (single pass).

     Recording event schema (in addition to the standard BFS
     events push / pop):
       `on_goal` — per goal-pop, with reason ∈ {expanded,
                   unreachable}. The `already_closed` reason
                   is unused (no per-goal restarts; each goal
                   is observed once at its pop).
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'KBFS',
                 is_recording: bool = False,
                 is_timing: bool = True) -> None:
        """
        ====================================================================
         Init private Attributes. No `h` kwarg is surfaced —
         BFS has no heuristic. The base `AlgoOMSPP` requires
         an `h` argument so a dummy `lambda s, g: 0` is passed
         internally (never invoked).
        ====================================================================
        """
        AlgoOMSPP.__init__(
            self,
            problem=problem,
            h=lambda s, g: 0,
            name=name,
            is_recording=is_recording,
            is_timing=is_timing,
        )
        self._inner: _MultiGoalBFS[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State] | None:
        """
        ====================================================================
         The inner BFS's `SearchStateSPP` bundle after `run()`
         completes. Available for post-hoc inspection of
         OPEN / CLOSED / g / parent.
        ====================================================================
        """
        return self._inner.search_state if self._inner else None

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Single-pass multi-goal BFS:
           1. Build a `goal_indices` map (state → list of input
              positions, to handle duplicate goals).
           2. Construct an inner `_MultiGoalBFS` configured with
              a remaining-set handle and an on-goal-pop
              callback.
           3. Run the inner once; the callback records each
              solution and emits `on_goal` per duplicate index.
           4. After the pass, mark any still-remaining goals as
              unreachable (cost = inf; reason = 'unreachable').
        ====================================================================
        """
        goal_indices: dict[State, list[int]] = {}
        for i, g in enumerate(self.problem.goals):
            goal_indices.setdefault(g, []).append(i)

        remaining: set[State] = set(goal_indices.keys())

        def on_goal_pop(state: State, cost: float) -> None:
            self._solutions[state] = SolutionSPP(cost=cost)
            for idx in goal_indices[state]:
                self._emit_on_goal(state, cost=cost,
                                   reason='expanded',
                                   goal_index=idx)

        self._inner = _MultiGoalBFS[State](
            problem=self.problem,
            remaining=remaining,
            on_goal_pop=on_goal_pop,
            name=f'{self.name}[inner]',
            is_recording=False,
        )
        self._inner._recorder = self._recorder
        self._inner.run()

        # Any goal still in `remaining` is unreachable from start.
        for state in list(remaining):
            self._solutions[state] = SolutionSPP(cost=float('inf'))
            for idx in goal_indices[state]:
                self._emit_on_goal(state, cost=float('inf'),
                                   reason='unreachable',
                                   goal_index=idx)

        return SolutionOMSPP(self._solutions)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the inner BFS's frontier and search-semantic
         counts into the algo's scaffold. Called by
         `AlgoOMSPP._run_post`. The inner FIFO frontier has no
         `cnt_decrease` counter (no decrease op), so the
         structural 0 is synthesized for the algo-level scaffold.
        ====================================================================
        """
        if self._inner is None:
            return
        fc = self._inner.search_state.frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        cnt_decrease = (fc['cnt_decrease']
                        if 'cnt_decrease' in fc else 0)
        self._counters.assign('cnt_decrease', cnt_decrease)
        # Search-semantic counters live on the inner algo's
        # _counters (incremented by AlgoSPP's loop and
        # _handle_child); mirror them through.
        ic = self._inner.counters
        self._counters.assign('cnt_expanded', ic['cnt_expanded'])
        self._counters.assign(
            'cnt_generated', ic['cnt_generated'])

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, goal: State) -> list[State]:
        """
        ====================================================================
         Walk the inner BFS's parent-pointer dict from `goal`
         back to the start. Returns `[]` if the goal was not
         reached.
        ====================================================================
        """
        if self._inner is None:
            return []
        shared = self._inner.search_state
        if goal not in shared.parent:
            return []
        path: list[State] = []
        cur: State | None = goal
        while cur is not None:
            path.append(cur)
            cur = shared.parent.get(cur)
        path.reverse()
        return path

    # ──────────────────────────────────────────────────
    #  Internal — event emitters
    # ──────────────────────────────────────────────────

    def _emit_on_goal(self,
                      goal: State,
                      cost: float,
                      reason: str,
                      goal_index: int) -> None:
        """
        ====================================================================
         Emit an `on_goal` event. Carries the goal index so
         duplicate goals remain distinguishable.
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
