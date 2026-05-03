from f_hs.algo.omspp._internal._aggregations import resolve_agg
from f_hs.algo.omspp.i_0_base.main import (
    AlgoOMSPP, PHASE_SEARCH, PHASE_UPDATE,
)
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)

# Phase tags for `_compute_F` counter routing.
# (Aliased to base names so the in-file callers stay readable.)
_PHASE_SEARCH = PHASE_SEARCH
_PHASE_UPDATE = PHASE_UPDATE


class KAStarAgg(Generic[State], AlgoOMSPP[State]):
    """
    ============================================================================
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

     Four orthogonal parameters control behaviour:
       `agg`          — Φ selector (string or callable).
       `is_lazy`      — defer F recomputation to pop time (lazy)
                        vs eager refresh immediately after each
                        goal is found.
       `is_opt`       — Stern §5.1.1 responsible-goal tracking.
                        Lazy: skip pop-time recompute when the
                        node's responsible goal is still active.
                        Eager: refresh only OPEN nodes whose
                        responsible goal was just removed.
                        Currently MIN / MAX only (singleton
                        responsible set).
       `store_vector` — each state stores [h_1(n), ..., h_k(n)]
                        as a vector (fast F recompute; O(k)
                        memory per state) vs only the current
                        aggregate (less memory; O(|active|)
                        h calls on each recompute). The vector
                        is filled only for goals that were
                        active at first-encounter time; closed
                        goals get a None sentinel and are never
                        read (the active set is
                        monotone-decreasing).

     Based on Stern et al. 2021 Algorithm 3 (§5.1, §5.1.1).

     Inherits the full f_cs Algo lifecycle from AlgoOMSPP —
     `algo.run()` returns a `SolutionOMSPP` (Mapping over
     `{goal: SolutionSPP}`); `algo.elapsed`, `algo.recorder`,
     `algo.counters`, `algo.solutions` all available.

     Per-run counters (8-counter scaffold from AlgoOMSPP):
       cnt_h_search   — h(n,t) calls in normal flow (push,
                        decrease-g, start seed).
       cnt_h_update   — h(n,t) calls in refresh flow (lazy
                        pop-recompute, eager `_refresh_all_F`).
       cnt_phi_search — `_compute_F` calls in normal flow.
       cnt_phi_update — `_compute_F` calls in refresh flow.
       cnt_push       — `frontier.push` calls.
       cnt_pop        — `frontier.pop` calls (heap-op cost).
       cnt_pop_stale  — pops that found stale F and re-inserted
                        (lazy mode only).
       cnt_decrease   — `frontier.decrease` calls.

     Recording event schema (push/pop/decrease_g plus):
       `on_goal`          — goal reached; reason='expanded' or
                            'unreachable'.
       `update_frontier`  — boundary before an eager F refresh;
                            carries num_nodes and next_goal_index.
       `update_heuristic` — per-node h/F update; fires during
                            eager refresh AND during lazy
                            re-insertion.
       `h_calc`           — single h(state, goal) evaluation;
                            value + phase ('search' / 'update').
       `phi_calc`         — single _compute_F call; carries phi
                            (the aggregated heuristic value) and
                            phase. Fires once per call, even when
                            no active goals (phi=0 then).
       `responsible_set`  — `self._responsible[state]` assigned
                            (only fires under is_opt=True).
       `refresh_skip`     — opt short-circuit fired; reason in
                            {'lazy_responsible_active',
                             'eager_responsible_unchanged'}.
       `pop_stale`        — lazy pop found stale F; carries
                            f_stored and f_recomputed (an
                            `update_heuristic` + re-push follows).
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 agg: str | Callable[[list[int]], int] = 'MIN',
                 is_lazy: bool = True,
                 is_opt: bool = False,
                 store_vector: bool = False,
                 name: str = 'KAStarAgg',
                 is_recording: bool = False,
                 is_timing: bool = True,
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        self._agg, self._agg_name = resolve_agg(agg)
        self._is_lazy: bool = is_lazy
        self._is_opt: bool = is_opt
        self._store_vector: bool = store_vector
        # is_opt: responsible-goal opt requires Φ whose
        # responsible set is the singleton arg-extremum.
        if is_opt and self._agg_name not in ('MIN', 'MAX'):
            raise ValueError(
                f'is_opt=True requires agg in MIN/MAX '
                f'(got {self._agg_name!r}).')
        # Per-run mutable state.
        self._frontier: FrontierPriority[State] = FrontierPriority[State]()
        self._g: dict[State, int] = {}
        self._parent: dict[State, State | None] = {}
        self._closed: set[State] = set()
        self._active_goals: set[State] = set()
        self._F_stored: dict[State, int] = {}
        # Vector slots for non-active goals at first-encounter
        # time are stored as None (sentinel). The active set is
        # monotone-decreasing, so a None slot is forever
        # unreachable via the `goal in self._active_goals`
        # filter in `_compute_F`.
        self._h_vector: dict[State, list[int | None]] = {}
        self._responsible: dict[State, State] = {}
        # Ordered list of all problem goals (stable for
        # store_vector indexing + PROJECTION ordering).
        self._all_goals: list[State] = []

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def agg(self) -> str:
        """String name of the aggregation ('MIN', 'MAX', ..., or 'CUSTOM')."""
        return self._agg_name

    @property
    def is_lazy(self) -> bool: return self._is_lazy

    @property
    def is_opt(self) -> bool: return self._is_opt

    @property
    def store_vector(self) -> bool: return self._store_vector

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Run the aggregative kA* loop.
        ====================================================================
        """
        self._reset_search_state()

        # Seed starts.
        for start in self.problem.starts:
            self._g[start] = 0
            self._parent[start] = None
            f = self._compute_F(start, phase=_PHASE_SEARCH)
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

            # Lazy: re-check F (skipped under is_opt when the
            # responsible goal is still active).
            if self._is_lazy:
                needs_recompute = True
                if self._is_opt:
                    resp = self._responsible.get(state)
                    if resp is None or resp in self._active_goals:
                        needs_recompute = False
                        self._emit_refresh_skip(
                            state,
                            reason='lazy_responsible_active')
                if needs_recompute:
                    actual_f = self._compute_F(
                        state, phase=_PHASE_UPDATE)
                    if actual_f != stored_f:
                        self._emit_pop_stale(
                            state, f_stored=stored_f,
                            f_recomputed=actual_f)
                        self._emit_update_heuristic(
                            state, h_old=stored_f - g_state,
                            h_new=actual_f - g_state)
                        self._F_stored[state] = actual_f
                        self._counters.inc('cnt_pop_stale')
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
                # beyond this one.
                self._closed.add(state)
                for child in self.problem.successors(state):
                    if child in self._closed:
                        continue
                    self._handle_child(parent=state, child=child)
                self._emit_on_goal(state, g=g_state,
                                   reason='expanded',
                                   goal_index=goal_index)
                if not self._is_lazy and self._active_goals:
                    # Eager refresh — the only Agg between-phase
                    # boundary. Lazy mode does NOT flip phase
                    # (its refresh work happens inline at pop
                    # time and structurally belongs to search).
                    self.phase = PHASE_UPDATE
                    self._refresh_all_F(
                        next_goal_index=self._next_active_index(),
                        just_removed_goal=state)
                    self.phase = PHASE_SEARCH
                if not self._active_goals:
                    break
                continue

            if state in self._closed:
                continue
            self._closed.add(state)

            # Expand.
            for child in self.problem.successors(state):
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

        return SolutionOMSPP(self._solutions)

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

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the frontier's heap-op counts into the algo's
         8-counter scaffold. Called by `AlgoOMSPP._run_post`
         after `_run` completes.
        ====================================================================
        """
        fc = self._frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        self._counters.assign('cnt_decrease', fc['cnt_decrease'])

    def _reset_search_state(self) -> None:
        """
        ====================================================================
         Reset per-run search bookkeeping. `_solutions` and the
         8 counters are reset by the base class's `_run_pre()`
         before `_run()` is called.
        ====================================================================
        """
        self._frontier = FrontierPriority[State]()
        self._g = {}
        self._parent = {}
        self._closed = set()
        self._all_goals = list(self.problem.goals)
        self._active_goals = set(self._all_goals)
        self._F_stored = {}
        self._h_vector = {}
        self._responsible = {}

    def _handle_child(self,
                      parent: State,
                      child: State) -> None:
        """
        ====================================================================
         Classical A* child handling adapted for kA*_agg.
        ====================================================================
        """
        new_g = self._g[parent] + self.problem.w(
            parent=parent, child=child)
        if child in self._frontier:
            if new_g < self._g[child]:
                self._g[child] = new_g
                self._parent[child] = parent
                f = self._compute_F(child, phase=_PHASE_SEARCH)
                self._F_stored[child] = f
                self._frontier.decrease(
                    state=child,
                    priority=(f, -new_g, child))
                self._emit_decrease_g(child, g=new_g, f=f,
                                      parent=parent)
        else:
            self._g[child] = new_g
            self._parent[child] = parent
            f = self._compute_F(child, phase=_PHASE_SEARCH)
            self._F_stored[child] = f
            self._frontier.push(
                state=child, priority=(f, -new_g, child))
            self._emit_push(child, g=new_g, f=f,
                            h=f - new_g,
                            parent=parent)

    def _compute_F(self,
                   state: State,
                   phase: str = _PHASE_SEARCH) -> int:
        """
        ====================================================================
         F(state) = g(state) + Φ(h_i(state) for i in active).

         Increments `cnt_h_*` and `cnt_phi_*` according to
         `phase`. When `is_opt=True`, also assigns
         `self._responsible[state]` to the active goal achieving
         the current arg-extremum (argmin for MIN, argmax for
         MAX).
        ====================================================================
        """
        if phase == _PHASE_SEARCH:
            self._counters.inc('cnt_phi_search')
        else:
            self._counters.inc('cnt_phi_update')

        g = self._g.get(state, 0)
        if not self._active_goals:
            self._emit_phi_calc(state, value=0, phase=phase)
            return int(g)

        if self._store_vector:
            if state not in self._h_vector:
                # Compute h only for currently-active goals;
                # store None for closed goals (never read,
                # since active set only shrinks).
                vec: list[int | None] = []
                n_h = 0
                for goal in self._all_goals:
                    if goal in self._active_goals:
                        v = int(self._h(state, goal))
                        self._emit_h_calc(state, goal, value=v,
                                          phase=phase)
                        vec.append(v)
                        n_h += 1
                    else:
                        vec.append(None)
                self._h_vector[state] = vec
                if phase == _PHASE_SEARCH:
                    self._counters.inc('cnt_h_search', n=n_h)
                else:
                    self._counters.inc('cnt_h_update', n=n_h)
            vec = self._h_vector[state]
            active_pairs = [(i, vec[i])
                            for i, goal in enumerate(self._all_goals)
                            if goal in self._active_goals]
        else:
            active_pairs = []
            for i, goal in enumerate(self._all_goals):
                if goal in self._active_goals:
                    v = int(self._h(state, goal))
                    self._emit_h_calc(state, goal, value=v,
                                      phase=phase)
                    active_pairs.append((i, v))
            n_h = len(active_pairs)
            if phase == _PHASE_SEARCH:
                self._counters.inc('cnt_h_search', n=n_h)
            else:
                self._counters.inc('cnt_h_update', n=n_h)

        if not active_pairs:
            self._emit_phi_calc(state, value=0, phase=phase)
            return int(g)

        active_h = [h for _, h in active_pairs]
        phi = self._agg(active_h)

        if self._is_opt:
            if self._agg_name == 'MIN':
                best_idx = min(
                    range(len(active_pairs)),
                    key=lambda j: active_pairs[j][1])
            else:  # 'MAX' (validated in __init__)
                best_idx = max(
                    range(len(active_pairs)),
                    key=lambda j: active_pairs[j][1])
            responsible_goal = self._all_goals[
                active_pairs[best_idx][0]]
            self._responsible[state] = responsible_goal
            self._emit_responsible_set(
                state, responsible=responsible_goal)

        self._emit_phi_calc(state, value=int(phi), phase=phase)
        return int(g + phi)

    def _refresh_all_F(self,
                       next_goal_index: int,
                       just_removed_goal: State | None = None,
                       ) -> None:
        """
        ====================================================================
         Eager refresh: drain the frontier, recompute F, re-push.

         When `is_opt=True` and `just_removed_goal` is given,
         only nodes whose responsible goal is the just-removed
         one have their F recomputed (and `update_heuristic`
         emitted); the rest keep their stored F. All OPEN nodes
         are re-pushed regardless (the heap has no increase-key,
         so we drain-and-rebuild).
        ====================================================================
        """
        states: list[State] = list(self._frontier)
        self._emit_update_frontier(
            num_nodes=len(states),
            next_goal_index=next_goal_index)
        self._frontier.clear()
        for s in states:
            old_f = self._F_stored[s]
            if (self._is_opt
                    and just_removed_goal is not None
                    and self._responsible.get(s)
                    != just_removed_goal):
                # Not affected; keep stored F (no recompute,
                # no `update_heuristic` event).
                self._emit_refresh_skip(
                    s, reason='eager_responsible_unchanged')
                new_f = old_f
            else:
                new_f = self._compute_F(s, phase=_PHASE_UPDATE)
                g_s = self._g[s]
                self._emit_update_heuristic(
                    s, h_old=old_f - g_s,
                    h_new=new_f - g_s)
                self._F_stored[s] = new_f
            g_s = self._g[s]
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

    def _emit_h_calc(self, state, goal, value, phase):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'h_calc', 'state': state, 'goal': goal,
            'value': int(value), 'phase': phase,
        })

    def _emit_phi_calc(self, state, value, phase):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'phi_calc', 'state': state,
            'value': int(value), 'phase': phase,
        })

    def _emit_responsible_set(self, state, responsible):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'responsible_set', 'state': state,
            'responsible': responsible,
        })

    def _emit_refresh_skip(self, state, reason):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'refresh_skip', 'state': state,
            'reason': reason,
        })

    def _emit_pop_stale(self, state, f_stored, f_recomputed):
        if not self._recorder.is_active:
            return
        self._recorder.record({
            'type': 'pop_stale', 'state': state,
            'f_stored': int(f_stored),
            'f_recomputed': int(f_recomputed),
        })
