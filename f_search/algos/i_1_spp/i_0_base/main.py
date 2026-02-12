from f_search.algos.i_0_base import AlgoBestFirst
from f_search.ds.state import StateBase
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP
from f_search.ds.data import DataBestFirst
from typing import Generic, TypeVar

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
                 data: Data,
                 name: str = 'AlgoSPP',
                 need_path: bool = True) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data,
                         name=name)
        self._need_path = need_path

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        if not self._data.frontier:
            self._discover(state=self.problem.start)
        while self._should_continue():
            self._select_best()
            if self._can_terminate():
                return
            self._explore_best()

    def _run_post(self) -> None:
        """
        ========================================================================
         Run the Post-Execution.
        ========================================================================
        """
        super()._run_post()
        is_valid = self._can_terminate()
        path = None
        if is_valid and self._need_path:
            path = self._data.path_to(self.problem.goal)
        self._output = SolutionSPP(problem=self.problem,
                                    is_valid=is_valid,
                                    stats=self._stats,
                                    path=path)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-State in Frontier.
        ========================================================================
        """
        return self._data.best == self.problem.goal
