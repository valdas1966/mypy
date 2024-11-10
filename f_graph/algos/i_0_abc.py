from f_abstract.processes.i_3_algo import Algorithm
from f_graph.problems.i_1_path import ProblemPath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Path = TypeVar('Path')
Data = TypeVar('Data')
Ops = TypeVar('Ops')


class AlgoPathABC(Generic[Problem, Path, Data, Ops],
                  Algorithm[Problem, Path, Data, Ops]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 input: Problem,
                 data: Data,
                 ops: Ops,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algorithm.__init__(self,
                           input=input,
                           data=data,
                           ops=ops,
                           name=name)
