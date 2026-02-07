from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.problems import ProblemSPP as Problem
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from f_search.ds.priority import PriorityGH
from f_search.heuristics import HeuristicsBase, HeuristicsManhattan
from f_search.ds.data import DataHeuristics
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: Problem,
                 name: str = 'AStar',
                 heuristics: HeuristicsBase[State, Problem] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         make_frontier=FrontierPriority,
                         make_data=DataHeuristics,
                         name=name)
        self._heuristics = heuristics if heuristics else HeuristicsManhattan(problem)

    def _discover(self, state: State) -> None:
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
            self._discover(state=succ)

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
        