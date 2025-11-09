from f_core.processes.i_0_abc import ProcessABC
from abc import abstractmethod
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(Generic[Output], ProcessABC):
    """
    ============================================================================
     ABC for Processes with OutputRequest.
    ============================================================================
    """

    def __init__(self,
                 name: str = 'ProcessOutput',
                 verbose: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessABC.__init__(self, name=name, verbose=verbose)
