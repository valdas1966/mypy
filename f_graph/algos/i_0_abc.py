from f_abstract.processes.i_1_output import ProcessOutput
from f_abstract.mixins.has_input import HasInput
from f_abstract.mixins.has_data import HasData
from f_graph.problems.i_1_path import ProblemPath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Path = TypeVar('Path')
Data = TypeVar('Data')


class AlgoPathABC(Generic[Problem, Path, Data],
                  ProcessOutput[Path],
                  HasInput[Problem],
                  HasData[Data]):
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
        ProcessOutput.__init__(self, name=name)
        HasInput.__init__(self, input=input)
        HasData.__init__(self, data=data)
