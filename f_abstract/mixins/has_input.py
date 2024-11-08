from typing import Generic, TypeVar

Input = TypeVar('Input')


class HasInput(Generic[Input]):
    """
    ============================================================================
     Mixin-Class for Processes with Input.
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
         Return the Process' Input.
        ========================================================================
        """
        return self._input
