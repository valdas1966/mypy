from f_cs.algo import Algo
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AlgoSPP(Generic[State], Algo[ProblemSPP[State], SolutionSPP]):
    """
    ========================================================================
     Base Algorithm for Shortest-Path-Problem.
    ========================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'AlgoSPP',
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        self._g: dict[State, float] = dict()
        self._parent: dict[State, State | None] = dict()
        self._closed: set[State] = set()
        self._goal_reached: State | None = None

    # ──────────────────────────────────────────────────
    #  The Search Loop (Classical Pseudocode)
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionSPP:
        """
        ====================================================================
         Run the Search Loop.
        ====================================================================
        """
        self._init_search()
        while self._has_frontier():
            state = self._pop()
            if self._is_goal(state):
                self._goal_reached = state
                return SolutionSPP(cost=self._g[state])
            self._close(state)
            for child in self.problem.successors(state):
                self._handle_child(parent=state,
                                   child=child)
        return SolutionSPP(cost=float('inf'))

    # ──────────────────────────────────────────────────
    #  Search Initialization
    # ──────────────────────────────────────────────────

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._g.clear()
        self._parent.clear()
        self._closed.clear()
        self._goal_reached = None
        self._goals_set = set(self.problem.goals)
        self._recorder.clear()
        for start in self.problem.starts:
            self._g[start] = 0.0
            self._parent[start] = None
            self._push(state=start)

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
        self._closed.add(state)

    def _handle_child(self,
                      parent: State,
                      child: State) -> None:
        """
        ====================================================================
         Handle a Child State discovered from Parent.
        ====================================================================
        """
        if child in self._closed:
            return
        new_g = (self._g[parent]
                 + self.problem.w(parent=parent,
                                  child=child))
        if not self._in_frontier(state=child):
            self._g[child] = new_g
            self._parent[child] = parent
            self._push(state=child)
        elif new_g < self._g[child]:
            self._g[child] = new_g
            self._parent[child] = parent
            self._decrease_g(state=child)

    # ──────────────────────────────────────────────────
    #  Frontier Operations (with recording)
    # ──────────────────────────────────────────────────

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push a State into the Frontier and record.
        ====================================================================
        """
        self._frontier_push(state=state)
        self._record_event(type='push', state=state)

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier and record.
        ====================================================================
        """
        state = self._frontier_pop()
        self._record_event(type='pop', state=state)
        return state

    def _decrease_g(self, state: State) -> None:
        """
        ====================================================================
         Update Priority and record.
        ====================================================================
        """
        self._frontier_decrease(state=state)
        self._record_event(type='decrease_g',
                           state=state)

    # ──────────────────────────────────────────────────
    #  Event Recording
    # ──────────────────────────────────────────────────

    def _record_event(self,
                      type: str,
                      state: State) -> None:
        """
        ====================================================================
         Record a Search Event. Auto-populates g, parent,
         and w from the Algorithm's internal state.
        ====================================================================
        """
        if not self._recorder:
            return
        event = dict(type=type,
                     state=state,
                     g=self._g[state])
        if type in ('push', 'decrease_g'):
            parent = self._parent[state]
            event['parent'] = parent
            if parent is not None:
                event['w'] = (self._g[state]
                              - self._g[parent])
        super()._record_event(**event)

    # ──────────────────────────────────────────────────
    #  Frontier (subclass must implement)
    # ──────────────────────────────────────────────────

    def _frontier_push(self, state: State) -> None:
        """
        ====================================================================
         Push a State into the Frontier.
        ====================================================================
        """
        raise NotImplementedError

    def _frontier_pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier.
        ====================================================================
        """
        raise NotImplementedError

    def _has_frontier(self) -> bool:
        """
        ====================================================================
         Return True if the Frontier is not empty.
        ====================================================================
        """
        raise NotImplementedError

    def _in_frontier(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is in the Frontier.
        ====================================================================
        """
        return False

    def _frontier_decrease(self, state: State) -> None:
        """
        ====================================================================
         Update the Priority of a State in the Frontier.
        ====================================================================
        """
        pass

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
        target = goal if goal is not None else self._goal_reached
        if target is None:
            return list()
        path: list[State] = list()
        current: State | None = target
        while current is not None:
            path.append(current)
            current = self._parent.get(current)
        path.reverse()
        return path
