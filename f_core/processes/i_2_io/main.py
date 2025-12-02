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
                 verbose: bool = False,
                 name: str = 'ProcessIO') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, input=input, verbose=verbose, name=name)
        ProcessOutput.__init__(self, verbose=verbose, name=name)

    def run(self) -> Output:
        """
        ========================================================================
         Run the Process and return the Output.
        ========================================================================
        """
        return ProcessOutput.run(self)
