from f_core.recorder.main import Recorder
from f_hs.algo.i_1_astar import AStar
from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.omspp._internal._single_goal_view import _SingleGoalView
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KAStarInc(Generic[State]):
    """
    ========================================================================
     Incremental kA* (kA*_inc) for the One-to-Many Shortest
     Path Problem.

     Runs k sequential A* sub-searches (one per goal) from a
     shared start. The SearchStateSPP bundle (OPEN, CLOSED,
     g-values, parent pointers) is **passed between
     sub-searches** — each iteration reuses what earlier
     iterations discovered.

     Between sub-search i and i+1:
       - The frontier is re-prioritised with h_{i+1} (auto-
         refresh via `AlgoSPP._frontier_dirty`).
       - If t_{i+1} is already in CLOSED (expanded by some
         earlier sub-search under consistent heuristics), the
         fast-path returns g[t_{i+1}] without a resume().

     Per Stern et al. (OMSPP/MOSPP submission) Theorem 1:
     assuming consistent heuristics, kA*_inc expands the same
     set of nodes as kA*_min up to tie-breaking — while
     computing only ONE heuristic per node per sub-search (vs
     `k` for kA*_min).

     Recording event schema (in addition to the standard
     AStar events push/pop/decrease_g):
       `on_goal`          — per goal, at sub-search termination.
                            reason ∈ {expanded, already_closed,
                            unreachable}.
       `update_frontier`  — boundary marker before priority
                            refresh on sub-search transition.
                            carries `num_nodes`.
       `update_heuristic` — per frontier state, old/new h-value.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'KAStarInc',
                 is_recording: bool = False,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `h` is a bi-arg callable `h(state, goal) -> int`. Each
         sub-search closes over its goal to produce a standard
         `Callable[[State], int]` for the inner AStar.

         Assumes consistent heuristics (required for kA*_inc's
         "same-nodes-as-kA*_min" guarantee and the closed-goal
         fast-path's correctness).
        ====================================================================
        """
        self._problem: ProblemSPP[State] = problem
        self._h: Callable[[State, State], int] = h
        self._name: str = name
        self._recorder: Recorder = Recorder(is_active=is_recording)
        self._solutions: dict[State, SolutionSPP] = {}
        self._shared_state: SearchStateSPP[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def problem(self) -> ProblemSPP[State]:
        """
        ====================================================================
         The input OMSPP problem.
        ====================================================================
        """
        return self._problem

    @property
    def name(self) -> str:
        """
        ====================================================================
         The algorithm instance name.
        ====================================================================
        """
        return self._name

    @property
    def recorder(self) -> Recorder:
        """
        ====================================================================
         The shared Recorder. Holds events from all k
         sub-searches interleaved with kA*_inc-specific meta
         events (on_goal, update_frontier, update_heuristic).
        ====================================================================
        """
        return self._recorder

    @property
    def solutions(self) -> dict[State, SolutionSPP]:
        """
        ====================================================================
         Per-goal SolutionSPP, populated by `run()`. Key ordering
         matches `problem.goals`.
        ====================================================================
        """
        return self._solutions

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

    def run(self) -> dict[State, SolutionSPP]:
        """
        ====================================================================
         Run k sub-searches sequentially, passing the
         SearchStateSPP bundle between them.

         Returns `{goal: SolutionSPP}` mapping. The same dict is
         accessible afterward via `self.solutions`.
        ====================================================================
        """
        self._solutions = {}
        self._shared_state = None
        prev_h: Callable[[State], int] | None = None
        goals = list(self._problem.goals)
        for i, goal in enumerate(goals):
            h_i = self._make_h_for(goal)

            # Fast-path: goal already expanded by an earlier
            # sub-search → its g is the optimal cost under
            # consistent-h assumption.
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
            # events (iterations 1+).
            if self._shared_state is not None:
                self._emit_frontier_transition(
                    shared=self._shared_state,
                    prev_h=prev_h,
                    new_h=h_i,
                    next_goal_index=i,
                )
                # Clear prior goal_reached so the new sub-search
                # starts from an uncommitted termination state.
                self._shared_state.goal_reached = None

            # Build the sub-problem (single-goal view).
            sub_problem = _SingleGoalView[State](
                base=self._problem, goal=goal)

            # Build the inner AStar with shared state + shared
            # recorder (swap after construction; AStar.__init__
            # would otherwise create its own private recorder).
            algo = AStar[State](
                problem=sub_problem,
                h=h_i,
                name=f'{self._name}[{i}]',
                is_recording=False,
                search_state=self._shared_state,
            )
            algo._recorder = self._recorder

            # Run for iteration 0; resume for 1+.
            if self._shared_state is None:
                sol = algo.run()
            else:
                sol = algo.resume()

            # Post-termination: if the goal was reached, AStar
            # returned without closing it or expanding its
            # successors (standard A* behavior — goal check
            # fires before `_close` + successor loop). For
            # kA*_inc continuity, the goal must be in CLOSED
            # and its successors on the frontier so subsequent
            # sub-searches can benefit. Force-expand here.
            reason = ('expanded' if sol.cost != float('inf')
                      else 'unreachable')
            if reason == 'expanded':
                shared = algo.search_state
                if goal not in shared.closed:
                    shared.closed.add(goal)
                    for child in sub_problem.successors(goal):
                        algo._handle_child(parent=goal,
                                           child=child)

            # Emit on_goal (after the force-expand so events
            # are in causal order: any push events from the
            # goal's children precede the on_goal marker).
            self._emit_on_goal(goal, cost=sol.cost,
                               reason=reason, goal_index=i)

            self._solutions[goal] = sol
            self._shared_state = algo.search_state
            prev_h = h_i
        return self._solutions

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
         Close over the current goal, producing a single-arg
         `Callable[[State], int]` suitable for AStar. The
         default-arg idiom `g=goal` captures the goal at lambda
         creation, avoiding the loop-variable late-binding
         pitfall.
        ====================================================================
        """
        h_outer = self._h
        return lambda s, g=goal: h_outer(s, g)

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

         `cost` is cast to int when finite; `float('inf')` for
         unreachable passes through unchanged.
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
            prev_h: Callable[[State], int],
            new_h: Callable[[State], int],
            next_goal_index: int,
            ) -> None:
        """
        ====================================================================
         Emit the `update_frontier` boundary event and one
         `update_heuristic` event per frontier state. Events
         fire BEFORE the actual refresh — they document the
         upcoming priority swap.

         `AlgoSPP._frontier_dirty` is True (set by the new
         AStar's __init__); on the first `resume()` it will
         invoke `refresh_priorities()` to rebuild the heap with
         the new h-derived priorities. The events here carry
         h_old / h_new so consumers don't need the pre-state.
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        frontier_states = list(shared.frontier)
        self._recorder.record(dict(
            type='update_frontier',
            num_nodes=len(frontier_states),
            next_goal_index=next_goal_index,
        ))
        for s in frontier_states:
            h_old = prev_h(s)
            h_new = new_h(s)
            self._recorder.record(dict(
                type='update_heuristic',
                state=s,
                h_old=int(h_old),
                h_new=int(h_new),
            ))
