from f_core.recorder.main import Recorder
from f_hs.algo.omspp._internal._aggregations import resolve_agg
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KAStarAgg(Generic[State]):
    """
    ========================================================================
     Aggregative kA* (kA*_agg) for the One-to-Many Shortest Path
     Problem.

     One best-first search toward all k goals simultaneously.
     F(n) = g(n) + Φ(h_i(n) for i in active_goals), where Φ is
     a heuristic aggregation function (MIN / MAX / AVG / RND /
     PROJECTION or a user-supplied callable).

     Active-goal set shrinks as goals are found: when t_i is
     expanded, its optimal path is recorded and t_i is removed
     from the active set. The priority function changes
     accordingly — F values of OPEN nodes may go stale.

     Three orthogonal parameters control behaviour:
       `agg`          — Φ selector (string or callable).
       `is_lazy`      — defer F recomputation to pop time (lazy)
                        vs eager refresh immediately after each
                        goal is found.
       `store_vector` — each state stores [h_1(n), ..., h_k(n)]
                        as a vector (fast F recompute; O(k)
                        memory per state) vs only the current
                        aggregate (less memory; O(|active|)
                        h calls on each recompute).

     Based on Stern et al. 2021 Algorithm 3.

     Recording event schema (standard push/pop/decrease_g plus):
       `on_goal`          — goal reached; reason='expanded' or
                            'unreachable'.
       `update_frontier`  — boundary before an eager F refresh;
                            carries num_nodes and next_goal_index.
       `update_heuristic` — per-node h/F update; fires during
                            eager refresh AND during lazy
                            re-insertion.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 agg: str | Callable[[list[int]], int] = 'MIN',
                 is_lazy: bool = True,
                 store_vector: bool = False,
                 name: str = 'KAStarAgg',
                 is_recording: bool = False,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._problem: ProblemSPP[State] = problem
        self._h: Callable[[State, State], int] = h
        self._agg, self._agg_name = resolve_agg(agg)
        self._is_lazy: bool = is_lazy
        self._store_vector: bool = store_vector
        self._name: str = name
        self._recorder: Recorder = Recorder(is_active=is_recording)
        # Per-run mutable state.
        self._solutions: dict[State, SolutionSPP] = {}
        self._frontier: FrontierPriority[State] = FrontierPriority[State]()
        self._g: dict[State, int] = {}
        self._parent: dict[State, State | None] = {}
        self._closed: set[State] = set()
        self._active_goals: set[State] = set()
        self._F_stored: dict[State, int] = {}
        self._h_vector: dict[State, list[int]] = {}
        # Ordered list of all problem goals (stable for
        # store_vector indexing + PROJECTION ordering).
        self._all_goals: list[State] = []

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def problem(self) -> ProblemSPP[State]: return self._problem

    @property
    def name(self) -> str: return self._name

    @property
    def recorder(self) -> Recorder: return self._recorder

    @property
    def solutions(self) -> dict[State, SolutionSPP]:
        return self._solutions

    @property
    def agg(self) -> str:
        """String name of the aggregation ('MIN', 'MAX', ..., or 'CUSTOM')."""
        return self._agg_name

    @property
    def is_lazy(self) -> bool: return self._is_lazy

    @property
    def store_vector(self) -> bool: return self._store_vector

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def run(self) -> dict[State, SolutionSPP]:
        """
        ====================================================================
         Run the aggregative kA* loop.
        ====================================================================
        """
        self._reset_search_state()

        # Seed starts.
        for start in self._problem.starts:
            self._g[start] = 0
            self._parent[start] = None
            f = self._compute_F(start)
            self._F_stored[start] = f
            self._emit_push(start, g=0, f=f,
                            h=f)  # h == F when g == 0
            self._frontier.push(state=start,
                                priority=(f, 0, start))

        # Main loop.
        while self._frontier and self._active_goals:
            state = self._frontier.pop()
            g_state = self._g[state]
            stored_f = self._F_stored[state]

            # Lazy: re-check F in case a goal was removed after
            # this state was pushed. If F changed (either
            # direction), re-insert with fresh priority.
            if self._is_lazy:
                actual_f = self._compute_F(state)
                if actual_f != stored_f:
                    self._emit_update_heuristic(
                        state, h_old=stored_f - g_state,
                        h_new=actual_f - g_state)
                    self._F_stored[state] = actual_f
                    self._frontier.push(
                        state=state,
                        priority=(actual_f, -g_state, state))
                    continue
                stored_f = actual_f

            # Emit pop AFTER lazy-refresh so the pop event
            # reflects the "final" F value we'll act on.
            self._emit_pop(state, g=g_state, f=stored_f)

            # Goal check against active goals.
            if state in self._active_goals:
                sol = SolutionSPP(cost=g_state)
                self._solutions[state] = sol
                goal_index = self._all_goals.index(state)
                self._active_goals.discard(state)
                # Force-expand: add goal to closed and push its
                # successors so subsequent sub-goals can reach
                # beyond this one. (AStar-style goal-pop-and-
                # return would leave the frontier starved.)
                self._closed.add(state)
                for child in self._problem.successors(state):
                    if child in self._closed:
                        continue
                    self._handle_child(parent=state, child=child)
                self._emit_on_goal(state, g=g_state,
                                   reason='expanded',
                                   goal_index=goal_index)
                if not self._is_lazy and self._active_goals:
                    self._refresh_all_F(
                        next_goal_index=self._next_active_index())
                if not self._active_goals:
                    break
                continue

            if state in self._closed:
                continue
            self._closed.add(state)

            # Expand.
            for child in self._problem.successors(state):
                if child in self._closed:
                    continue
                self._handle_child(parent=state, child=child)

        # Remaining active goals are unreachable.
        for goal in list(self._active_goals):
            sol = SolutionSPP(cost=float('inf'))
            self._solutions[goal] = sol
            goal_index = self._all_goals.index(goal)
            self._emit_on_goal(goal, g=float('inf'),
                               reason='unreachable',
                               goal_index=goal_index)
            self._active_goals.discard(goal)

        return self._solutions

    def reconstruct_path(self, goal: State) -> list[State]:
        """
        ====================================================================
         Walk parents from `goal` back to start. Returns [] if
         the goal was never reached.
        ====================================================================
        """
        if goal not in self._parent:
            return []
        path: list[State] = []
        cur: State | None = goal
        while cur is not None:
            path.append(cur)
            cur = self._parent.get(cur)
        path.reverse()
        return path

    # ──────────────────────────────────────────────────
    #  Core Ops
    # ──────────────────────────────────────────────────

    def _reset_search_state(self) -> None:
        self._solutions = {}
        self._frontier = FrontierPriority[State]()
        self._g = {}
        self._parent = {}
        self._closed = set()
        self._all_goals = list(self._problem.goals)
        self._active_goals = set(self._all_goals)
        self._F_stored = {}
        self._h_vector = {}

    def _handle_child(self,
                      parent: State,
                      child: State) -> None:
        """
        ====================================================================
         Classical A* child handling adapted for kA*_agg.
        ====================================================================
        """
        new_g = self._g[parent] + self._problem.w(
            parent=parent, child=child)
        if child in self._frontier:
            if new_g < self._g[child]:
                self._g[child] = new_g
                self._parent[child] = parent
                f = self._compute_F(child)
                self._F_stored[child] = f
                self._frontier.decrease(
                    state=child,
                    priority=(f, -new_g, child))
                self._emit_decrease_g(child, g=new_g, f=f,
                                      parent=parent)
        else:
            self._g[child] = new_g
            self._parent[child] = parent
            f = self._compute_F(child)
            self._F_stored[child] = f
            self._frontier.push(
                state=child, priority=(f, -new_g, child))
            self._emit_push(child, g=new_g, f=f,
                            h=f - new_g,
                            parent=parent)

    def _compute_F(self, state: State) -> int:
        """
        ====================================================================
         F(state) = g(state) + Φ(h_i(state) for i in active).
        ====================================================================
        """
        g = self._g.get(state, 0)
        if not self._active_goals:
            return g
        if self._store_vector:
            if state not in self._h_vector:
                self._h_vector[state] = [
                    int(self._h(state, goal))
                    for goal in self._all_goals
                ]
            vec = self._h_vector[state]
            active_h = [vec[i]
                        for i, goal in enumerate(self._all_goals)
                        if goal in self._active_goals]
        else:
            active_h = [int(self._h(state, goal))
                        for goal in self._all_goals
                        if goal in self._active_goals]
        phi = self._agg(active_h) if active_h else 0
        return int(g + phi)

    def _refresh_all_F(self, next_goal_index: int) -> None:
        """
        ====================================================================
         Eager refresh: drain the frontier, recompute every F
         with the reduced active-goal set, re-push. Emits
         `update_frontier` and one `update_heuristic` per state.
        ====================================================================
        """
        states: list[State] = list(self._frontier)
        self._emit_update_frontier(
            num_nodes=len(states),
            next_goal_index=next_goal_index)
        self._frontier.clear()
        for s in states:
            old_f = self._F_stored[s]
            new_f = self._compute_F(s)
            g_s = self._g[s]
            self._emit_update_heuristic(
                s, h_old=old_f - g_s, h_new=new_f - g_s)
            self._F_stored[s] = new_f
            self._frontier.push(state=s,
                                priority=(new_f, -g_s, s))

    def _next_active_index(self) -> int:
        """
        ====================================================================
         Return the first still-active goal's index in the
         original goals list — used to label the post-refresh
         state via `next_goal_index` on `update_frontier`.
         Returns -1 if no active goals remain.
        ====================================================================
        """
        for i, g in enumerate(self._all_goals):
            if g in self._active_goals:
                return i
        return -1

    # ──────────────────────────────────────────────────
    #  Event Emission
    # ──────────────────────────────────────────────────

    def _emit_push(self, state, g, f, h, parent=None):
        if not self._recorder.is_active:
            return
        event = {
            'type': 'push', 'state': state,
            'g': int(g), 'h': int(h), 'f': int(f),
            'parent': parent,
        }
        self._recorder.record(event)

    def _emit_pop(self, state, g, f):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'pop', 'state': state,
            'g': int(g), 'h': int(f) - int(g), 'f': int(f),
        })

    def _emit_decrease_g(self, state, g, f, parent):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'decrease_g', 'state': state,
            'g': int(g), 'h': int(f) - int(g), 'f': int(f),
            'parent': parent,
        })

    def _emit_on_goal(self, goal, g, reason, goal_index):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'on_goal', 'state': goal,
            'g': int(g) if g != float('inf') else g,
            'reason': reason, 'goal_index': goal_index,
        })

    def _emit_update_frontier(self, num_nodes, next_goal_index):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'update_frontier',
            'num_nodes': int(num_nodes),
            'next_goal_index': int(next_goal_index),
        })

    def _emit_update_heuristic(self, state, h_old, h_new):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'update_heuristic', 'state': state,
            'h_old': int(h_old), 'h_new': int(h_new),
        })
