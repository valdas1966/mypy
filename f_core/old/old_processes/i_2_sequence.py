from f_core.processes.i_1_input import ProcessInput, Input
from dataclasses import dataclass
from typing import Type, Generic, TypeVar, Iterable

Process = TypeVar('Process', bound=ProcessInput)


@dataclass
class DataSequence(Generic[Process, Input]):
    """ 
    ============================================================================
     Data for a sequence of Processes.
    ============================================================================
    """
    process: Type[Process]
    inputs: Iterable[Input]


class ProcessSequence(ProcessInput[DataSequence]):
    """
    ============================================================================
     Process a sequence of Processes.
    ============================================================================
    """
    def __init__(self,
                 _input: DataSequence,
                 verbose: bool = True,
                 name: str = 'Process Sequence') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, verbose=verbose, name=name)
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
            name = f'{self._name}[{i+1}\{len(self._inputs)}]'
            process = self._process(_input=_input, name=name)
            process.run()
        self._run_post()
