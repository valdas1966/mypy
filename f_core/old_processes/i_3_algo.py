from f_core.processes.i_2_io import ProcessIO
from typing import Generic, TypeVar

Input = TypeVar('InputRequest')
Output = TypeVar('OutputRequest')
Data = TypeVar('Data')
Ops = TypeVar('Ops')


class Algorithm(Generic[Input, Output, Data, Ops],
                ProcessIO[Input, Output]):

    def __init__(self,
                 input: Input,
                 data: Data,
                 ops: Ops,
                 name: str = 'Algorithm') -> None:
        ProcessIO.__init__(self, input=input, name=name)
        self._data = data
        self._ops = ops
