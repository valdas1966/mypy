from f_cs.algo import Algo
from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.frontier.i_0_base.main import FrontierBase
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
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
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        # Per-search dynamic state (frontier + g + parent + closed +
        # goal_reached). Mutated during the loop, exposed read-only
        # via `search_state` for cross-instance peeking (bidirectional).
        self._search: SearchStateSPP[State] = SearchStateSPP(
            frontier=frontier,
        )
        # Cached lookup set, derived from the (immutable) problem.
        # Lives on the algo (not on _search) because it never changes
        # across run / resume cycles.
        self._goals_set: set[State] = set()

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
         preserved. Used by OMSPP-iterative pumping and by
         bidirectional search.
        ====================================================================
        """
        self._run_pre()
        self._output = self._search_loop()
        self._run_post()
        return self._output

    # ──────────────────────────────────────────────────
    #  Search Initialization
    # ──────────────────────────────────────────────────

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._search.clear()
        self._goals_set = set(self.problem.goals)
        self._recorder.clear()
        for start in self.problem.starts:
            self._search.g[start] = 0.0
            self._search.parent[start] = None
            self._push(state=start)

    # ──────────────────────────────────────────────────
    #  Search Loop (Classical Pseudocode)
    # ──────────────────────────────────────────────────

    def _search_loop(self) -> SolutionSPP:
        """
        ====================================================================
         Pump the search loop until a Goal is popped or the
         Frontier is exhausted. Does NOT initialize — callable
         after _init_search (via _run) or directly (via resume).
        ====================================================================
        """
        while self._search.frontier:
            state = self._pop()
            if self._is_goal(state):
                self._search.goal_reached = state
                return SolutionSPP(cost=self._search.g[state])
            self._close(state)
            for child in self.problem.successors(state):
                self._handle_child(parent=state,
                                   child=child)
        return SolutionSPP(cost=float('inf'))

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
                      state: State) -> None:
        """
        ====================================================================
         Record a Search Event. Auto-populates g (as int) and
         parent from the Algorithm's internal state. Edge cost w
         is intentionally NOT recorded — it's derivable from
         g(child) - g(parent) and duplicates structural info
         already carried by parent.
        ====================================================================
        """
        if not self._recorder:
            return
        event = dict(type=type,
                     state=state,
                     g=int(self._search.g[state]))
        if type in ('push', 'decrease_g'):
            event['parent'] = self._search.parent[state]
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
