from typing import Generic, TypeVar

Output = TypeVar('Output')


class HasOutput(Generic[Output]):
    """
    ============================================================================
     Mixin-Class for Processes with Output.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._output: Output | None = None

    @property
    def output(self) -> Output:
        """
        ========================================================================
         Return the Process' Output.
        ========================================================================
        """
        return self._output
