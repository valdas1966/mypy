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
                 _input: Input,
                 name: str = 'Process IO') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, name=name)
