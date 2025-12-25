from f_core.processes.i_0_abc import ProcessABC
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(Generic[Output], ProcessABC):
    """
    ============================================================================
     ABC for Processes with Output.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 verbose: bool = False,
                 name: str = 'ProcessOutput') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._output: Output | None = None
        ProcessABC.__init__(self, verbose=verbose, name=name)

    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        self._run_pre()
        self._run()
        self._run_post()
        return self._output

    def _run_post(self) -> None:
        """
        ========================================================================
         Run the Post-Run Commands.
        ========================================================================
        """
        ProcessABC._run_post(self)
