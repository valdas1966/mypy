from f_abstract.processes.i_1_output import ProcessOutput
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')
Data = TypeVar('Data')


class Algorithm(Generic[Input, Output, Data],
                ProcessOutput[Output]):

    def __init__(self,
                 input: Input,
                 data: Data,
                 name: str = 'Algorithm') -> None:
        ProcessOutput.__init__(self, name=name)
        self._input = input
        self._data = data

    @property
    def input(self) -> Input:
        return self._input

    @property
    def data(self) -> Data:
        return self._data
