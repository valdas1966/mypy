from f_search.algos.i_0_base import AlgoSearch
from f_search.solutions import SolutionOMSPP
from f_search.problems import ProblemOMSPP
from f_search.ds import StateBase as State
from f_search.ds.data import DataSearch
from f_search.stats import StatsSearch
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemOMSPP)
Solution = TypeVar('Solution', bound=SolutionOMSPP)
Stats = TypeVar('Stats', bound=StatsSearch)
Data = TypeVar('Data', bound=DataSearch)


class AlgoOMSPP(Generic[Problem, Solution, Stats, Data],
                AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for One-to-Many Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    cls_stats = StatsSearch
    cls_data = DataSearch

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 name: str = 'AlgoOMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            data=data,
                            name=name)
        self._goals_active: list[State] = []
        self._sub_solutions: dict[State, Solution] = dict()

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        AlgoSearch._run_pre(self)
        self._goals_active = self._problem.goals
        self._sub_solutions = dict()

    def _create_solution(self) -> SolutionOMSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        self._run_post()
        return SolutionOMSPP(sub_solutions=self._sub_solutions,
                             elapsed=self._stats.elapsed)
