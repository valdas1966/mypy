from f_core.processes.i_0_base import ProcessBase
from typing import Generic, TypeVar

Input = TypeVar('Input')


class ProcessInput(Generic[Input], ProcessBase):
    """
    ============================================================================
    ABC for Processes with Input.
    ============================================================================
    """

    def __init__(self,
                _input: Input,
                verbose: bool = False,
                name: str = 'Process Input') -> None:
        """
        ========================================================================
        Init private Attributes.
        ========================================================================
        """
        ProcessBase.__init__(self, verbose=verbose, name=name)
        self._input = _input

    @property
    def input(self) -> Input:
        """
        ========================================================================
        Return the Input of the Process.
        ========================================================================
        """
        return self._input
