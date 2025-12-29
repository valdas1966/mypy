from f_core.processes.i_0_abc import ProcessABC
from typing import Generic, TypeVar


Input = TypeVar('Input')

class ProcessInput(Generic[Input], ProcessABC):
    """
    ============================================================================
     ABC for Processes with Input.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 input: Input,
                 name: str = 'Process Input') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._input = input
        ProcessABC.__init__(self, name=name)

    @property
    def input(self) -> Input:
        """
        ========================================================================
         Return the Input of the Process.
        ========================================================================
        """
        return self._input
        