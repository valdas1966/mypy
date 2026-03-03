from f_search.algos.i_1_spp.i_1_astar.main import AStar, State, Data
from f_search.problems import ProblemSPP as Problem
from f_search.heuristics import HeuristicsProtocol
from typing import Generic


class AStarReusable(Generic[State], AStar[State]):
    """
    ============================================================================
     AStar with reusable Data for chaining searches.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: Problem,
                 name: str = 'AStarReusable',
                 data: Data[State] = None,
                 heuristics: HeuristicsProtocol[State] = None,
                 need_path: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AStar.__init__(self, problem=problem, name=name)
        if data:
            self._data = data
        if heuristics:
            self._heuristics = heuristics
        self._need_path = need_path
