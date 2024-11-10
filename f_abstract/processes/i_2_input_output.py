from f_abstract.processes.i_1_input import ProcessInput
from f_abstract.processes.i_1_output import ProcessOutput
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class ProcessIO(Generic[Input, Output],
                ProcessInput[Input],
                ProcessOutput[Output]):

    def __init__(self, input: Input, name: str = 'Process IO') -> None:
        ProcessInput.__init__(self, input=input, name=name)
