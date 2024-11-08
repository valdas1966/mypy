from f_abstract.processes.i_0_abc import ProcessABC
from abc import abstractmethod
from typing import Generic, TypeVar

Output = TypeVar('Output')


class ProcessOutput(ProcessABC, Generic[Output]):

    def __init__(self, name: str = 'ProcessOutput') -> None:
        ProcessABC.__init__(self, name=name)

    @abstractmethod
    def run(self, **kwargs) -> Output:
        pass
