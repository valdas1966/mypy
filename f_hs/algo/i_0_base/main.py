from f_cs.algo import Algo
from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.frontier.i_0_base.main import FrontierBase
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter_ns
from typing import Any, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AlgoSPP(Generic[State], Algo[ProblemSPP[State], SolutionSPP]):
    """
    ============================================================================
     Base Algorithm for Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 frontier: FrontierBase[State],
                 name: str = 'AlgoSPP',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `search_state` — optional pre-built SearchStateSPP to
         inject (e.g., seed a mid-search state for a test, or
         feed an iterative OMSPP sub-search with warm g/parent
         dicts). When supplied, the `frontier` argument is
         ignored (the caller's `search_state.frontier` wins).
         Consumers who inject should call `resume()` rather
         than `run()`, since `run() → _init_search` clears the
         bundle before pumping.
        ====================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        # Per-search dynamic state (frontier + g + parent + closed +
        # goal_reached + cache_hit). Mutated during the loop, exposed
        # via `search_state` for cross-instance peeking and for
        # caller-driven seeding.
        self._search: SearchStateSPP[State] = (
            search_state if search_state is not None
            else SearchStateSPP(frontier=frontier))
        # Cached lookup set, derived from the (immutable) problem.
        # Populated at init (not only in _init_search) so a
        # caller who uses `resume()` straight after construction
        # still has a working goal check.
        self._goals_set: set[State] = set(self.problem.goals)
        # Dirty flag — when a caller injects a SearchStateSPP
        # whose frontier entries were pushed with priorities
        # computed against a stale heuristic or goal, the next
        # resume() refreshes them. Cleared after refresh; also
        # cleared by `_init_search` (which rebuilds the frontier
        # from scratch, making any stale priorities irrelevant).
        self._frontier_dirty: bool = search_state is not None
        # Seed the event-duration clock so pre-search events
        # (e.g., `propagate` emitted from pathmax before
        # `_run_pre` fires) can compute a valid `duration`.
        # `_run_pre` will reset this later for search timing.
        self._event_prev_ns: int = perf_counter_ns()

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State]:
        """
        ====================================================================
         The dynamic per-search state. Read-access for consumers
         that need to inspect frontier/closed/g across instances
         (e.g. bidirectional search), and the resumability anchor.
        ====================================================================
        """
        return self._search

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionSPP:
        """
        ====================================================================
         Initialize the search and run the loop. Public entry via
         the inherited run().
        ====================================================================
        """
        self._init_search()
        return self._search_loop()

    def resume(self) -> SolutionSPP:
        """
        ====================================================================
         Continue the search from current state without
         re-initializing. Reuses ProcessBase's lifecycle plumbing
         (timing reset + output capture) but skips _init_search,
         so frontier / closed / g / parent / recorder are
         preserved.

         If the frontier is marked dirty (caller injected a
         SearchStateSPP at __init__), refresh priorities before
         pumping — re-computing `_priority(state)` for every
         state on the frontier. Refresh is O(n log n) on the
         frontier size; subsequent resume() calls see a clean
         frontier and skip the refresh.

         Used by OMSPP-iterative pumping, bidirectional search,
         and caller-seeded recording tests.
        ====================================================================
        """
        if self._frontier_dirty:
            self.refresh_priorities()
        self._run_pre()
        self._output = self._search_loop()
        self._run_post()
        return self._output

    def refresh_priorities(self) -> None:
        """
        ====================================================================
         Recompute the priority of every State currently on the
         frontier and rebuild the frontier with the fresh values.
         Safe with non-monotone changes (priorities may go up
         OR down) — uses drain-and-push rather than `decrease`,
         since FrontierPriority's `decrease` rejects higher
         priorities.

         Does NOT emit recorder events (the refresh is setup,
         not a search step). Clears the dirty flag on success.
        ====================================================================
        """
        states: list[State] = list(self._search.frontier)
        self._search.frontier.clear()
        for s in states:
            self._search.frontier.push(
                state=s,
                priority=self._priority(state=s),
            )
        self._frontier_dirty = False

    # ──────────────────────────────────────────────────
    #  Search Initialization
    # ──────────────────────────────────────────────────

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.

         **Recorder is NOT cleared here** (as of Phase 2b's
         pre-search `propagate` events). Events recorded before
         `run()` — e.g., from `propagate_pathmax` — must persist
         into the search log so consumers see the full timeline.
         Callers who want a fresh log across `run()` invocations
         should call `self.recorder.clear()` explicitly.
        ====================================================================
        """
        self._search.clear()
        self._goals_set = set(self.problem.goals)
        for start in self.problem.starts:
            self._search.g[start] = 0.0
            self._search.parent[start] = None
            self._push(state=start)
        # Frontier is freshly rebuilt with current priorities —
        # any stale-priority concerns from an injected seed are
        # moot after a full init.
        self._frontier_dirty = False

    # ──────────────────────────────────────────────────
    #  Search Loop (Classical Pseudocode)
    # ──────────────────────────────────────────────────

    def _search_loop(self) -> SolutionSPP:
        """
        ====================================================================
         Pump the search loop until a Goal is popped or the
         Frontier is exhausted. Does NOT initialize — callable
         after _init_search (via _run) or directly (via resume).

         `_early_exit` runs after pop and before the goal check;
         it short-circuits the loop when a subclass (AStar with
         HCached) can terminate via perfect-h on the popped state.
        ====================================================================
        """
        while self._search.frontier:
            state = self._pop()
            sol = self._early_exit(state=state)
            if sol is not None:
                return sol
            if self._is_goal(state):
                self._search.goal_reached = state
                return SolutionSPP(cost=self._search.g[state])
            self._close(state)
            for child in self.problem.successors(state):
                self._handle_child(parent=state,
                                   child=child)
        return SolutionSPP(cost=float('inf'))

    # ──────────────────────────────────────────────────
    #  Early-Exit Hook (subclass override)
    # ──────────────────────────────────────────────────

    def _early_exit(self, state: State) -> SolutionSPP | None:
        """
        ====================================================================
         Subclass hook — return a SolutionSPP to short-circuit
         the loop immediately after popping `state`, or None to
         continue with the normal goal-check + expansion. Default:
         never short-circuit. AStar overrides to terminate on
         an HCached perfect-h hit.
        ====================================================================
        """
        return None

    # ──────────────────────────────────────────────────
    #  Core Operations
    # ──────────────────────────────────────────────────

    def _is_goal(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is a Goal.
        ====================================================================
        """
        return state in self._goals_set

    def _close(self, state: State) -> None:
        """
        ====================================================================
         Close the State (mark as expanded).
        ====================================================================
        """
        self._search.closed.add(state)

    def _handle_child(self,
                      parent: State,
                      child: State) -> None:
        """
        ====================================================================
         Handle a Child State discovered from Parent.
        ====================================================================
        """
        if child in self._search.closed:
            return
        new_g = (self._search.g[parent]
                 + self.problem.w(parent=parent,
                                  child=child))
        if child not in self._search.frontier:
            self._search.g[child] = new_g
            self._search.parent[child] = parent
            self._push(state=child)
        elif new_g < self._search.g[child]:
            self._search.g[child] = new_g
            self._search.parent[child] = parent
            self._decrease_g(state=child)

    # ──────────────────────────────────────────────────
    #  Frontier Wrappers (with recording)
    # ──────────────────────────────────────────────────

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push a State into the Frontier and record.
        ====================================================================
        """
        self._search.frontier.push(
            state=state,
            priority=self._priority(state=state),
        )
        self._record_event(type='push', state=state)

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier and record.
        ====================================================================
        """
        state = self._search.frontier.pop()
        self._record_event(type='pop', state=state)
        return state

    def _decrease_g(self, state: State) -> None:
        """
        ====================================================================
         Update Priority in the Frontier and record.
        ====================================================================
        """
        self._search.frontier.decrease(
            state=state,
            priority=self._priority(state=state),
        )
        self._record_event(type='decrease_g', state=state)

    # ──────────────────────────────────────────────────
    #  Priority (subclass override)
    # ──────────────────────────────────────────────────

    def _priority(self, state: State) -> Any:
        """
        ====================================================================
         Return the Priority for a State. Default: None (FIFO).
         Subclasses (e.g. AStar) override to compute a priority
         tuple, e.g. (f, -g, state).
        ====================================================================
        """
        return None

    # ──────────────────────────────────────────────────
    #  Event Recording
    # ──────────────────────────────────────────────────

    def _record_event(self,
                      type: str,
                      state: State,
                      **extra) -> None:
        """
        ====================================================================
         Record a Search Event.

         Auto-fill policy:
           - `g` (as int): added for push / pop / decrease_g.
             Skipped for other types (propagate and future
             pre-/post-search events) — they may fire with a
             state not yet in `self._search.g`.
           - `parent`: added for push / decrease_g. Skipped for
             pop (the Recording Principle's `parent not in event`
             ⇒ "parenthood isn't applicable here"). Skipped for
             non-search types too — callers pass their own via
             **extra when semantically meaningful (e.g.,
             propagate events name the source as `parent`).

         `**extra` is merged onto the event dict, so callers can
         add arbitrary fields (h_parent for propagate, etc.).
         Edge cost w is NOT recorded — it's derivable.
        ====================================================================
        """
        if not self._recorder:
            return
        event = dict(type=type, state=state)
        if type in ('push', 'pop', 'decrease_g'):
            event['g'] = int(self._search.g[state])
        if type in ('push', 'decrease_g'):
            event['parent'] = self._search.parent[state]
        event.update(extra)
        super()._record_event(**event)

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self,
                         goal: State | None = None
                         ) -> list[State]:
        """
        ====================================================================
         Reconstruct the Path from Start to Goal.
        ====================================================================
        """
        target = (goal if goal is not None
                  else self._search.goal_reached)
        if target is None:
            return list()
        path: list[State] = list()
        current: State | None = target
        while current is not None:
            path.append(current)
            current = self._search.parent.get(current)
        path.reverse()
        return path
