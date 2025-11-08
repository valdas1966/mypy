from f_cs.algo import Algo
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from typing import Generic, TypeVar
from abc import abstractmethod

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)


class AlgoSearch(Generic[Problem, Solution],
                 Algo[Problem, Solution]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, verbose=verbose, name=name)

    @abstractmethod
    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass
