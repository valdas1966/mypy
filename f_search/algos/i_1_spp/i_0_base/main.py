from f_search.algos.i_0_base import AlgoBestFirst
from f_search.ds.state import StateBase
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP
from f_search.ds.frontier import FrontierBase as Frontier
from f_search.ds.data import DataBestFirst
from typing import Generic, TypeVar, Callable

State = TypeVar('State', bound=StateBase)
Data = TypeVar('Data', bound=DataBestFirst)


class AlgoSPP(Generic[State, Data],
              AlgoBestFirst[ProblemSPP, SolutionSPP, State, Data]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP,
                 make_frontier: Callable[[], Frontier[State]],
                 make_data: Callable[[], Data],
                 name: str = 'AlgoSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         make_frontier=make_frontier,
                         make_data=make_data,
                         name=name)

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._discover(state=self.problem.start)
        while self._should_continue():
            self._select_best()
            if self._can_terminate():
                self._output = self._create_solution()
                return
            self._explore_best()
        self._output = self._create_failure()

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-State in Frontier.
        ========================================================================
        """
        return self._data.best == self.problem.goal

    def _create_solution(self) -> SolutionSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        path = self._data.path_to(self.problem.goal)
        return SolutionSPP(problem=self.problem,
                           is_valid=True,
                           stats=self._stats,
                           path=path)

    def _create_failure(self) -> SolutionSPP:
        """
        ========================================================================
         Create a Failure Solution.
        ========================================================================
        """
        return SolutionSPP(problem=self.problem,
                           is_valid=False,
                           stats=self._stats,
                           path=None)

        