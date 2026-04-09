from f_cs.algo import Algo
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar
from time import time

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
                self._record_event(type='pop',
                                   state=state,
                                   g=self._g[state],
                                   skipped=True)
                continue
            self._record_event(type='pop',
                               state=state,
                               g=self._g[state],
                               skipped=False)
            if self._is_goal(state):
                self._goal_reached = state
                cost = self._g[state]
                self._record_event(type='goal_found',
                                   state=state,
                                   cost=cost)
                return SolutionSPP(cost=cost)
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
        self._recorder.clear()
        for start in self.problem.starts:
            self._g[start] = 0.0
            self._parent[start] = None
            self._push(state=start)
            self._record_event(type='push',
                               state=start,
                               g=0.0,
                               parent=None)

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
            self._record_event(type='generate',
                               parent=parent,
                               child=child,
                               relaxed=False)
            return
        edge_cost = self._edge_cost(parent=parent, child=child)
        new_g = self._g[parent] + edge_cost
        old_g = self._g.get(child, float('inf'))
        if child not in self._g or new_g < old_g:
            self._g[child] = new_g
            self._parent[child] = parent
            self._push(state=child)
            self._record_event(type='generate',
                               parent=parent,
                               child=child,
                               edge_cost=edge_cost,
                               new_g=new_g,
                               old_g=old_g,
                               relaxed=True)
            self._record_event(type='push',
                               state=child,
                               g=new_g,
                               parent=parent)
        else:
            self._record_event(type='generate',
                               parent=parent,
                               child=child,
                               edge_cost=edge_cost,
                               new_g=new_g,
                               old_g=old_g,
                               relaxed=False)

    def _record_event(self, **kwargs) -> None:
        """
        ====================================================================
         Record a Search Event with Elapsed Time.
        ====================================================================
        """
        if self._recorder:
            kwargs['elapsed'] = time() - self._time_start
            self._recorder.record(kwargs)

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
        t_start = time()
        target = goal if goal is not None else self._goal_reached
        if target is None:
            return list()
        path: list[State] = list()
        current: State | None = target
        while current is not None:
            path.append(current)
            current = self._parent.get(current)
        path.reverse()
        if self._recorder:
            self._recorder.record(
                dict(type='reconstruct_path',
                     goal=target,
                     path_length=len(path),
                     elapsed=time() - t_start)
            )
        return path
