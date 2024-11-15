from f_abstract.processes.i_0_abc import ProcessABC
from abc import abstractmethod
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(Generic[Output], ProcessABC):
    """
    ============================================================================
     ABC for Processes with Output.
    ============================================================================
    """

    def __init__(self, name: str = 'ProcessOutput') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessABC.__init__(self, name=name)

    @abstractmethod
    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        pass
