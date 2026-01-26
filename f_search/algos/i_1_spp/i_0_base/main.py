from f_search.algos.i_0_base import AlgoSearch
from f_search.ds.data import DataBestFirst
from f_search.stats import StatsSearch as Stats
from f_search.problems import ProblemSPP as Problem
from f_search.solutions import SolutionSPP as Solution
from f_search.ds.frontier import FrontierBase as Frontier
from typing import Generic, TypeVar

Data = TypeVar('Data', bound=DataBestFirst)


class AlgoSPP(Generic[Data], AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    cls_stats = Stats
    cls_data = Data

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 type_frontier: type = Frontier,
                 name: str = 'AlgoSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data,
                         type_frontier=type_frontier,
                         name=name)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-State in Frontier.
        ========================================================================
        """
        return self._data.best == self._problem.goal

    def _create_solution(self, is_valid: bool) -> Solution:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        path = self._data.path_to(self._problem.goal)
        return Solution(is_valid=is_valid,
                        stats=self._stats,
                        path=path)

        