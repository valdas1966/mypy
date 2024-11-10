from f_abstract.processes.i_0_abc import ProcessABC
from typing import Generic, TypeVar

Input = TypeVar('Input')


class ProcessInput(Generic[Input], ProcessABC):

    def __init__(self,
                 input: Input,
                 name: str = 'Process Input') -> None:
        ProcessABC.__init__(self, name=name)
        self._input = input

    @property
    def input(self) -> Input:
        return self._input
