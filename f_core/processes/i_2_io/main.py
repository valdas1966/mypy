from f_core.processes.i_1_input import ProcessInput
from f_core.processes.i_1_output import ProcessOutput
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class ProcessIO(Generic[Input, Output],
                ProcessInput[Input],
                ProcessOutput[Output]):
    """
    ============================================================================
     ABC for Processes with Input and Output.
    ============================================================================
    """

    def __init__(self,
                 input: Input,
                 name: str = 'ProcessIO',
                 is_recording: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, input=input, name=name,
                              is_recording=is_recording)
        ProcessOutput.__init__(self, name=name,
                               is_recording=is_recording)

    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        return ProcessOutput.run(self)
