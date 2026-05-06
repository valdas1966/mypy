from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_omspp._single_goal_view import _SingleGoalView
from f_hs.algo.i_1_omspp.i_0_base.main import (
    AlgoOMSPP, PHASE_SEARCH, PHASE_UPDATE,
)
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KAStarInc(Generic[State], AlgoOMSPP[State]):
    """
    ============================================================================
     Incremental kA* (kA*_inc) for the One-to-Many Shortest
     Path Problem.

     Runs k sequential A* sub-searches (one per goal) from a
     shared start. The SearchStateSPP bundle (OPEN, CLOSED,
     g-values, parent pointers) is **passed between
     sub-searches** — each iteration reuses what earlier
     iterations discovered.

     Between sub-search i and i+1:
       - For non-last reached goals: the goal is **re-pushed**
         to OPEN with its optimal g (lazy re-expansion). When
         a future sub-search pops it, A*'s standard close+expand
         fires naturally — no orchestrator-side force-expand.
         The last reached goal is NOT re-pushed (no consumer).
       - The frontier is re-prioritised with h_{i+1} (priority
         refresh, called explicitly with phase='update' so
         h-calls are counted as `cnt_h_update`).
       - Fast-path: if t_{i+1} was a prior sub-search's goal
         (in `self._solutions`) → reason='already_reached'; if
         it was popped+closed as collateral by an earlier
         sub-search (in `shared.closed`) → reason='already_closed'.
         Either way no resume() runs.

     Per Stern et al. (OMSPP/MOSPP submission) Theorem 1:
     assuming consistent heuristics, kA*_inc expands the same
     set of nodes as kA*_min up to tie-breaking — while
     computing only ONE heuristic per node per sub-search (vs
     `k` for kA*_min).

     Inherits the f_cs Algo lifecycle from AlgoOMSPP —
     `algo.run()` returns `SolutionOMSPP` (Mapping over
     `{goal: SolutionSPP}`); `algo.elapsed`, `algo.recorder`,
     `algo.counters` all available.

     Recording event schema (in addition to the standard
     AStar events push/pop/decrease_g):
       `on_goal`          — per goal, at sub-search termination.
                            reason ∈ {expanded, already_closed,
                            unreachable, already_reached}.
       `update_frontier`  — boundary marker before priority
                            refresh on sub-search transition.
                            carries `num_nodes` and
                            `next_goal_index`. Per-state
                            `update_heuristic` events are NOT
                            emitted — the silent re-keying via
                            `refresh_priorities` is observable
                            through `cnt_h_update`.
    ============================================================================
    """

    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search', 'cnt_h_update'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'KAStarInc',
                 is_recording: bool = False,
                 is_timing: bool = True,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `h` is a bi-arg callable `h(state, goal) -> int`. Each
         sub-search closes over its goal to produce a standard
         `Callable[[State], int]` for the inner AStar — wrapped
         with a counter that routes calls to `cnt_h_search` or
         `cnt_h_update` based on `self._phase` (the same field
         drives the structural-phase time bucket).

         Assumes consistent heuristics (required for kA*_inc's
         "same-nodes-as-kA*_min" guarantee and the closed-goal
         fast-path's correctness).
        ====================================================================
        """
        AlgoOMSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        self._shared_state: SearchStateSPP[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State] | None:
        """
        ====================================================================
         The shared SearchStateSPP bundle after run() completes.
         Available for post-hoc inspection of OPEN/CLOSED/g/parent.
        ====================================================================
        """
        return self._shared_state

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Run k sub-searches sequentially, passing the
         SearchStateSPP bundle between them.
        ====================================================================
        """
        self._shared_state = None
        # Default phase is 'search' (set by base in _run_pre).
        goals = list(self.problem.goals)
        for i, goal in enumerate(goals):
            h_i = self._make_h_for(goal)

            # Fast-path: this goal's optimal cost is already
            # known if (a) it was a previous sub-search's goal
            # (in self._solutions — its sub-search popped it
            # and finalized g), or (b) it was popped+closed as
            # collateral by an earlier sub-search (in
            # shared.closed; consistent-h ⇒ g is optimal). The
            # two cases get distinct event reasons for benchmark
            # readability.
            if goal in self._solutions:
                sol = self._solutions[goal]
                self._emit_on_goal(goal, cost=sol.cost,
                                   reason='already_reached',
                                   goal_index=i)
                continue
            if (self._shared_state is not None
                    and goal in self._shared_state.closed):
                cost = self._shared_state.g[goal]
                sol = SolutionSPP(cost=cost)
                self._emit_on_goal(goal, cost=cost,
                                   reason='already_closed',
                                   goal_index=i)
                self._solutions[goal] = sol
                continue

            # Inter-sub-search transition: priority refresh
            # events (iterations 1+). All h-calls during this
            # block are counted as `cnt_h_update`; flip drives
            # both counter routing AND the elapsed_update bucket.
            if self._shared_state is not None:
                self.phase = PHASE_UPDATE
                self._emit_frontier_transition(
                    shared=self._shared_state,
                    next_goal_index=i,
                )
                # Clear prior goal_reached so the new sub-search
                # starts from an uncommitted termination state.
                self._shared_state.goal_reached = None

            # Build the sub-problem (single-goal view).
            sub_problem = _SingleGoalView[State](
                base=self.problem, goal=goal)

            # Build the inner AStar with shared state + shared
            # recorder (swap after construction; AStar.__init__
            # would otherwise create its own private recorder).
            algo = AStar[State](
                problem=sub_problem,
                h=h_i,
                name=f'{self.name}[{i}]',
                is_recording=False,
                search_state=self._shared_state,
            )
            algo._recorder = self._recorder

            # Iterations 1+: explicitly run refresh_priorities
            # under phase='update' so the h-calls performed by
            # the auto-refresh land in `cnt_h_update` rather
            # than `cnt_h_search`, and the wall-clock lands in
            # `elapsed_update`. After the explicit refresh,
            # `_frontier_dirty` is False so resume() skips its
            # own auto-refresh.
            if self._shared_state is None:
                self.phase = PHASE_SEARCH
                sol = algo.run()
            else:
                self.phase = PHASE_UPDATE
                algo.refresh_priorities()
                self.phase = PHASE_SEARCH
                sol = algo.resume()

            # Accumulate the inner sub-search's search-semantic
            # counters (each AStar instance owns its own
            # cnt_expanded / cnt_generated; sum across all
            # sub-searches gives the total over the whole INC run).
            ic = algo.counters
            self._counters.inc(
                'cnt_expanded', n=ic['cnt_expanded'])
            self._counters.inc(
                'cnt_generated', n=ic['cnt_generated'])

            # Post-termination: AStar returned at goal-pop
            # without closing the goal or generating its
            # successors. Lazy re-push design — for non-last
            # reached goals, push the goal back onto OPEN with
            # its optimal g; the next sub-search's natural
            # close+expand will handle it if/when its f under
            # h_{i+1} clears C_{i+1}. The last goal is NEVER
            # re-pushed — no future sub-search would consume
            # the work.
            reason = ('expanded' if sol.cost != float('inf')
                      else 'unreachable')

            # Emit on_goal first so the goal-completion marker
            # precedes any "preparation for next sub-search"
            # events (the lazy re-push, if any).
            self._emit_on_goal(goal, cost=sol.cost,
                               reason=reason, goal_index=i)
            self._solutions[goal] = sol

            if (reason == 'expanded'
                    and i < len(goals) - 1):
                # Re-push under the just-finished search's h_i;
                # the next transition's refresh_priorities()
                # will re-key it under h_{i+1}.
                algo._push(state=goal)

            self._shared_state = algo.search_state
        return SolutionOMSPP(self._solutions)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the shared frontier's heap-op counts into the
         algo's 8-counter scaffold. Called by
         `AlgoOMSPP._run_post` after `_run` completes.
        ====================================================================
        """
        if self._shared_state is None:
            return
        fc = self._shared_state.frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        self._counters.assign('cnt_decrease', fc['cnt_decrease'])

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, goal: State) -> list[State]:
        """
        ====================================================================
         Walk the shared parent-pointer dict from `goal` back to
         the start. Works for both `expanded` goals and
         `already_closed` fast-path goals — parent pointers are
         set during the sub-search that first closed the state.
        ====================================================================
        """
        if self._shared_state is None:
            return []
        if goal not in self._shared_state.parent:
            return []
        path: list[State] = []
        cur: State | None = goal
        while cur is not None:
            path.append(cur)
            cur = self._shared_state.parent.get(cur)
        path.reverse()
        return path

    # ──────────────────────────────────────────────────
    #  Internal
    # ──────────────────────────────────────────────────

    def _make_h_for(
            self, goal: State
            ) -> Callable[[State], int]:
        """
        ====================================================================
         Close over the current goal AND wrap with a phase-aware
         counter — every h-call routes to `cnt_h_search` or
         `cnt_h_update` based on `self._phase` at call time.
        ====================================================================
        """
        h_outer = self._h

        def h_wrapped(s: State, g: State = goal) -> int:
            v = h_outer(s, g)
            if self._phase == PHASE_SEARCH:
                self._counters.inc('cnt_h_search')
            else:
                self._counters.inc('cnt_h_update')
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

    def _emit_frontier_transition(
            self,
            shared: SearchStateSPP[State],
            next_goal_index: int,
            ) -> None:
        """
        ====================================================================
         Emit the `update_frontier` boundary event marking the
         sub-search transition. No per-state cluster — the
         actual heuristic re-keying happens via
         `refresh_priorities()` and is observable through its
         h-call counter (`cnt_h_update`) and the `push` events
         it emits during drain-and-rebuild.
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        self._recorder.record(dict(
            type='update_frontier',
            num_nodes=len(shared.frontier),
            next_goal_index=next_goal_index,
        ))
