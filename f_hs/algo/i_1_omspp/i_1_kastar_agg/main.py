from f_hs.algo.i_1_omspp.i_1_kastar_agg._aggregations import resolve_agg
from f_hs.algo.i_1_omspp.i_0_base.main import (
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
       cnt_h_search   — h(n,t) calls in normal flow (start
                        seed, first-time push in `_handle_child`,
                        decrease-g).
       cnt_h_update   — h(n,t) calls in refresh flow: lazy
                        pop-recompute, eager
                        `_refresh_priorities`, AND the goal
                        re-push at goal-find (h is recomputed
                        under the newly-shrunken active set).
       cnt_phi_search — `_compute_F` calls in normal flow.
       cnt_phi_update — `_compute_F` calls in refresh flow
                        (lazy pop-recompute, eager
                        `_refresh_priorities`, goal re-push).
       cnt_push       — `frontier.push` calls.
       cnt_pop        — `frontier.pop` calls (heap-op cost).
       cnt_pop_stale  — pops that found stale F and re-inserted
                        (lazy mode only).
       cnt_decrease   — `frontier.decrease` calls.

     Recording event schema — minimal, INC-aligned (5 types):
       `push`             — first-time push (initial seed +
                            `_handle_child` first-encounter
                            branch) AND the lazy re-push of any
                            non-last goal at goal-find. Eager
                            bulk re-push (in `_refresh_priorities`)
                            and lazy stale re-push are silent.
                            Stream's `push` count = `cnt_generated`
                            + (number of non-last goals reached).
       `pop`              — non-stale pop (real expansion) only.
                            Lazy stale pops are silent; stream's
                            `pop` count = `cnt_pop − cnt_pop_stale`.
       `decrease_g`       — child relaxation; one per `cnt_decrease`.
       `on_goal`          — goal reached; reason='expanded' or
                            'unreachable'. Emitted BEFORE the
                            lazy re-push (INC-symmetric goal-
                            handling order: pop → on_goal →
                            push (re-push) → update_frontier).
       `update_frontier`  — eager-only boundary marker before the
                            bulk refresh; carries num_nodes and
                            next_goal_index. Lazy mode does NOT
                            emit (no between-phase moment exists).

     Goal handling — lazy re-push (INC-symmetric):

     At goal-pop the goal is recorded, removed from active_goals,
     and re-pushed under the shrunken active set's Φ — NOT
     force-expanded. Successors of the goal are reached via
     other states during the search; if a remaining active goal
     can only be optimally reached *through* the just-found
     goal, the re-pushed entry will re-pop in priority order
     and the standard close+expand fires (in the non-goal
     branch). Under consistent h with MIN/MAX aggregation, this
     guarantees correctness: f_new(t_i) ≤ C*(t_j) whenever t_j's
     optimal path passes through t_i, so t_i must re-pop before
     t_j is found. The last active goal is NEVER re-pushed (no
     consumer). The pattern is one-to-one symmetric to KAStarInc's
     lazy re-push (which defers goal close+expand to a future
     sub-search via `algo._push(state=goal)` before transition).

     Refresh-internal events (`update_heuristic`, `pop_stale`,
     `h_calc`, `phi_calc`, `responsible_set`, `refresh_skip`)
     were removed for INC-consistency and recorder-overhead
     reduction. The aggregate `cnt_h_*` / `cnt_phi_*` /
     `cnt_pop_stale` counters preserve the work-type
     observability.
    ============================================================================
    """

    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search', 'cnt_h_update'),
        ('cnt_phi_search', 'cnt_phi_update'),
        ('cnt_push', 'cnt_pop',
         'cnt_pop_stale', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed'),
    )

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
            self._counters.inc('cnt_generated')

        # Main loop.
        while self._frontier and self._active_goals:
            state = self._frontier.pop()
            g_state = self._g[state]
            stored_f = self._F_stored[state]

            # Lazy: re-check F (skipped under is_opt when the
            # responsible goal is still active). Stale re-push
            # is silent — no event emitted (consistent with
            # kA*-INC's silent refresh re-pushes); cnt_pop_stale
            # tracks the count.
            if self._is_lazy:
                needs_recompute = True
                if self._is_opt:
                    resp = self._responsible.get(state)
                    if resp is None or resp in self._active_goals:
                        needs_recompute = False
                if needs_recompute:
                    actual_f = self._compute_F(
                        state, phase=_PHASE_UPDATE)
                    if actual_f != stored_f:
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
                # Lazy re-push (INC-symmetric). NOT force-
                # expanded: the goal is not added to closed and
                # its successors are not generated here. If a
                # remaining active goal's optimal path passes
                # through this goal, the re-pushed entry will
                # re-pop in priority order and the standard
                # close+expand fires in the non-goal branch.
                # The last active goal is NEVER re-pushed (no
                # consumer for its expansion).
                self._emit_on_goal(state, g=g_state,
                                   reason='expanded',
                                   goal_index=goal_index)
                if not self._active_goals:
                    break
                # Re-push under the shrunken active set's Φ.
                # PHASE_UPDATE — h / Φ are recomputed under the
                # newly-shrunken active goal set; that work is
                # refresh-typed (responding to active-set
                # change), not search-typed. The wall-clock
                # still falls into elapsed_search (the work
                # happens inside the search loop), matching the
                # lazy stale-pop precedent: counters tag WORK
                # TYPE; elapsed buckets tag STRUCTURAL PHASE.
                new_f = self._compute_F(state, phase=_PHASE_UPDATE)
                self._F_stored[state] = new_f
                self._frontier.push(
                    state=state,
                    priority=(new_f, -g_state, state))
                self._emit_push(state, g=g_state, f=new_f,
                                h=new_f - g_state,
                                parent=self._parent.get(state))
                if not self._is_lazy:
                    # Eager refresh — the only Agg between-phase
                    # boundary. Lazy mode does NOT flip phase
                    # (its refresh work happens inline at pop
                    # time and structurally belongs to search).
                    # `just_re_pushed_state=state`: skip the
                    # redundant recompute of the goal we just
                    # re-pushed (its F was computed under the
                    # exact same active set on line 293).
                    self.phase = PHASE_UPDATE
                    self._refresh_priorities(
                        next_goal_index=self._next_active_index(),
                        just_removed_goal=state,
                        just_re_pushed_state=state)
                    self.phase = PHASE_SEARCH
                continue

            if state in self._closed:
                continue
            self._closed.add(state)
            self._counters.inc('cnt_expanded')

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
            self._counters.inc('cnt_generated')
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
                    active_pairs.append((i, v))
            n_h = len(active_pairs)
            if phase == _PHASE_SEARCH:
                self._counters.inc('cnt_h_search', n=n_h)
            else:
                self._counters.inc('cnt_h_update', n=n_h)

        if not active_pairs:
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

        return int(g + phi)

    def _refresh_priorities(self,
                            next_goal_index: int,
                            just_removed_goal: State | None = None,
                            just_re_pushed_state: State | None = None,
                            ) -> None:
        """
        ====================================================================
         Eager refresh: drain the frontier, recompute F, re-push.

         Same structural operation as
         `AlgoSPP.refresh_priorities()` (drain + clear +
         re-push with fresh priorities) — named symmetrically
         so the vocabulary is unified across INC (calls
         `algo.refresh_priorities()` on its inner AStar) and
         AGG-eager (this method). Diverges from the AlgoSPP
         version only in bookkeeping: maintains `_F_stored`
         and applies the `is_opt` short-circuit. Re-pushes are
         silent (no `push` events emitted) — only the
         `update_frontier` boundary marker fires before the
         drain.

         When `is_opt=True` and `just_removed_goal` is given,
         only nodes whose responsible goal is the just-removed
         one have their F recomputed; the rest keep their
         stored F. All OPEN nodes are re-pushed regardless
         (the heap has no increase-key, so we drain-and-
         rebuild).

         When `just_re_pushed_state` is given, that state's F
         was just freshly computed under the post-removal
         active set by the goal re-push site (line 293) —
         skip the recompute (the value is identical). This
         saves one `_compute_F` per non-last goal-find in
         `is_opt=False` configs (in `is_opt=True` the
         responsible-skip rule already covers it, since the
         re-pushed goal's responsible is updated to a
         remaining active goal during the re-push).
        ====================================================================
        """
        states: list[State] = list(self._frontier)
        self._emit_update_frontier(
            num_nodes=len(states),
            next_goal_index=next_goal_index)
        self._frontier.clear()
        for s in states:
            old_f = self._F_stored[s]
            if (just_re_pushed_state is not None
                    and s == just_re_pushed_state):
                # Just re-pushed by the goal-find branch — F
                # was computed under the new active set on
                # line 293; recomputing yields the same value.
                new_f = old_f
            elif (self._is_opt
                    and just_removed_goal is not None
                    and self._responsible.get(s)
                    != just_removed_goal):
                # Not affected; keep stored F (no recompute).
                new_f = old_f
            else:
                new_f = self._compute_F(s, phase=_PHASE_UPDATE)
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

