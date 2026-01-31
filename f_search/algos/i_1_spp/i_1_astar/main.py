from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.problems import ProblemSPP
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from f_search.ds.priority import PriorityGH
from typing import Generic, TypeVar, Callable

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 heuristics: Callable[[State], int],
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         make_frontier=FrontierPriority,
                         name=name)
        self._heuristics = heuristics

    def _discover(self, state: State, parent: State = None) -> None:
        """
        ========================================================================
         Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        # Set State's Parent
        data.set_best_to_be_parent_of(state=state)
        # Calculate the heuristic distance from state to goal
        data.dict_h[state] = self._heuristics(state=state)
        # Calculate the priority of the State (in the Frontier)
        priority = PriorityGH(key=state.key,
                                   g=data.dict_g[state],
                                   h=data.dict_h[state])
        # Push State to Frontier
        data.frontier.push(state=state, priority=priority)

    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        if succ in self._data.frontier:
            if self._need_relax(succ=succ):
                self._relax(succ=succ)
        else:
            self._discover(state=succ, parent=self._data.best)

    def _need_relax(self, succ: State) -> bool:
        """
        ========================================================================
         Return True if through Best-State, the Succ can be reached with a
          lower cost through its current parent.
        ========================================================================
        """
        # Aliases
        g_succ = self._data.dict_g[succ]
        g_best = self._data.dict_g[self._data.best]
        return g_succ > g_best + 1

    def _relax(self, succ: State) -> None:
        """
        ========================================================================
         Relax the Successor.
        ========================================================================
        """
        self._stats.relaxed += 1
        # Aliases
        data = self._data
        # Set the Successor's Parent to the Best-State
        data.set_best_to_be_parent_of(state=succ)
        priority = PriorityGH(key=succ.key,
                                   g=data.dict_g[succ],
                                   h=data.dict_h[succ])
        data.frontier.update(state=succ, priority=priority)
        