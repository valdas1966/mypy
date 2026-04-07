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

    # ──────────────────────────────────────────────────────
    #  The Search Loop
    # ──────────────────────────────────────────────────────

    def _run(self) -> SolutionSPP:
        """
        ====================================================================
         Run the Search Loop.
        ====================================================================
        """
        self._init_search()
        while self._has_open():
            state = self._pop()
            if state in self._closed:
                continue
            if self._is_goal(state):
                self._goal_reached = state
                return SolutionSPP(cost=self._g[state])
            self._close(state)
            for child in self.problem.successors(state):
                self._handle_child(parent=state, child=child)
        return SolutionSPP(cost=float('inf'))

    # ──────────────────────────────────────────────────────
    #  Search Initialization
    # ──────────────────────────────────────────────────────

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
        for start in self.problem.starts:
            self._g[start] = 0.0
            self._parent[start] = None
            self._push(state=start)

    # ──────────────────────────────────────────────────────
    #  Core Operations
    # ──────────────────────────────────────────────────────

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
        new_g = self._g[parent] + self._edge_cost(
            parent=parent, child=child
        )
        if child not in self._g or new_g < self._g[child]:
            self._g[child] = new_g
            self._parent[child] = parent
            self._push(state=child)

    def _edge_cost(self,
                   parent: State,
                   child: State) -> float:
        """
        ====================================================================
         Return the Edge Cost from Parent to Child.
        ====================================================================
        """
        return 1.0

    # ──────────────────────────────────────────────────────
    #  Frontier (subclass must implement)
    # ──────────────────────────────────────────────────────

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push a State into the Frontier.
        ====================================================================
        """
        raise NotImplementedError

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier.
        ====================================================================
        """
        raise NotImplementedError

    def _has_open(self) -> bool:
        """
        ====================================================================
         Return True if the Frontier is not empty.
        ====================================================================
        """
        raise NotImplementedError

    # ──────────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────────

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
