from f_search.algos.i_0_base import AlgoSearch
from f_search.solutions import SolutionOMSPP, SolutionSPP
from f_search.problems import ProblemOMSPP
from f_search.ds.state import StateBase
from f_search.ds.data import DataBestFirst
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)
Data = TypeVar('Data', bound=DataBestFirst)


class AlgoOMSPP(AlgoSearch[ProblemOMSPP, SolutionOMSPP],
                Generic[State, Data]):
    """
    ============================================================================
     Base for One-to-Many Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AlgoOMSPP',
                 **kwargs) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            name=name)
        self._goals_active: list[State]
        self._sub_solutions: list[SolutionSPP]

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        AlgoSearch._run_pre(self)
        self._goals_active = list(self.problem.goals)
        self._sub_solutions = list()

    def _run_post(self) -> None:
        """
        ========================================================================
         Run Post-Processing.
        ========================================================================
        """
        super()._run_post()
        self._output = SolutionOMSPP(problem=self.problem,
                                     subs=self._sub_solutions,
                                     elapsed=self._stats.elapsed)
