from typing import Generic, TypeVar

Output = TypeVar('OutputRequest')


class HasOutput(Generic[Output]):
    """
    ============================================================================
     Mixin-Class for Processes with OutputRequest.
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
         Return the Process' OutputRequest.
        ========================================================================
        """
        return self._output
