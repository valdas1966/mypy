from f_core.processes.i_0_base import ProcessBase
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(ProcessBase, Generic[Output]):
    """
    ============================================================================
     ABC for Processes with Output.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 name: str = 'ProcessOutput',
                 is_recording: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._output: Output | None = None
        ProcessBase.__init__(self, name=name, is_recording=is_recording)

    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        self._run_pre()
        self._output = self._run()
        self._run_post()
        return self._output

    def _run_post(self) -> None:
        """
        ========================================================================
         Run the Post-Run Commands.
        ========================================================================
        """
        super()._run_post()
