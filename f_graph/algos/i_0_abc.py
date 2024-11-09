from f_abstract.processes.i_2_algo import Algorithm
from f_graph.problems.i_1_path import ProblemPath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Path = TypeVar('Path')
Data = TypeVar('Data')


class AlgoPathABC(Generic[Problem, Path, Data],
                  Algorithm[Problem, Path, Data]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 input: Problem,
                 data: Data,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algorithm.__init__(self,
                           input=input,
                           data=data,
                           name=name)
