from f_core.processes.i_0_abc import ProcessABC
from typing import Generic, TypeVar

Input = TypeVar('InputRequest')


class ProcessInput(Generic[Input], ProcessABC):
    """
    ============================================================================
     ABC for Processes with InputRequest.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = 'Process InputRequest') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessABC.__init__(self, name=name)
        self._input = _input

    @property
    def input(self) -> Input:
        """
        ========================================================================
         Return the InputRequest of the Process.
        ========================================================================
        """
        return self._input
