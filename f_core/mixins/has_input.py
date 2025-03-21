from typing import Generic, TypeVar

Input = TypeVar('InputRequest')


class HasInput(Generic[Input]):
    """
    ============================================================================
     Mixin-Class for Processes with InputRequest.
    ============================================================================
    """

    def __init__(self, input: Input = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._input = input

    @property
    def input(self) -> Input:
        """
        ========================================================================
         Return the Process' InputRequest.
        ========================================================================
        """
        return self._input
