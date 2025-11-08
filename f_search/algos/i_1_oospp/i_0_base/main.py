from f_search.algos.i_0_base.main import AlgoSearch
from f_search.problems import ProblemOOSPP
from f_search.solutions import SolutionOOSPP
from typing import Generic, TypeVar
from abc import abstractmethod

Problem = TypeVar('Problem', bound=ProblemOOSPP)
Solution = TypeVar('Solution', bound=SolutionOOSPP) 


class AlgoOOSPP(Generic[Problem, Solution],
                AlgoSearch[Problem, Solution]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoOOSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            verbose=verbose,
                            name=name)

    @abstractmethod
    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass
