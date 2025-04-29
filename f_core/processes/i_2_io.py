from f_core.processes.i_1_input import ProcessInput
from f_core.processes.i_1_output import ProcessOutput
from typing import Generic, TypeVar

Input = TypeVar('InputRequest')
Output = TypeVar('OutputRequest')


class ProcessIO(Generic[Input, Output],
                ProcessInput[Input],
                ProcessOutput[Output]):
    """
    ============================================================================
     ABC for Processes with InputRequest and OutputRequest.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 verbose: bool = False,
                 name: str = 'Process IO') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, verbose=verbose, name=name)
