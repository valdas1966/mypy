from f_search.algos.i_0_base import AlgoBestFirst
from f_search.ds.state import StateBase
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP
from f_search.ds.frontier import FrontierBase as Frontier
from typing import Generic, TypeVar, Callable

State = TypeVar('State', bound=StateBase)


class AlgoSPP(Generic[State],
              AlgoBestFirst[ProblemSPP, SolutionSPP, State]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP,
                 make_frontier: Callable[[], Frontier[State]],
                 name: str = 'AlgoSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         make_frontier=make_frontier,
                         name=name)

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
        return SolutionSPP(is_valid=True,
                           stats=self._stats,
                           path=path)

    def _create_failure(self) -> SolutionSPP:
        """
        ========================================================================
         Create a Failure Solution.
        ========================================================================
        """
        return SolutionSPP(is_valid=False,
                           stats=self._stats,
                           path=None)

        