from f_core.processes.i_1_input import ProcessInput, Input
from dataclasses import dataclass
from typing import Type, Generic, TypeVar

Process = TypeVar('Process', bound=ProcessInput)


@dataclass
class DataSequence(Generic[Process, Input]):
    """
    ============================================================================
     Data for a sequence of Processes.
    ============================================================================
    """
    process: Type[Process]
    inputs: list[Input]


class ProcessSequence(ProcessInput[DataSequence]):
    """
    ============================================================================
     Process a sequence of Processes.
    ============================================================================
    """
    def __init__(self,
                 _input: DataSequence,
                 name: str = 'Process Sequence') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, name=name)
        self._process = _input.process
        self._inputs = _input.inputs

    def run(self) -> None:
        """
        ========================================================================
         Run the sequence of Processes.
        ========================================================================    
        """
        self._run_pre()
        for i, _input in enumerate(self._inputs):
            name = f'{self._name}[{i+1}]'
            process = self._process(_input=_input, name=name)
            process.run()
        self._run_post()
