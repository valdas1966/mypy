from f_core.processes.i_0_base import ProcessBase
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(Generic[Output], ProcessBase):
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
        ProcessBase.__init__(self, name=name, verbose=verbose)

    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        pass
