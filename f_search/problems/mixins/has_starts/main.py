from f_search.ds.state import StateCell as State


class HasStarts:
    """
    ============================================================================
     Mixin for Problems with multiple Start-States.
    ============================================================================
    """

    def __init__(self,
                 starts: list[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._starts: list[State] = starts

    @property
    def starts(self) -> list[State]:
        """
        ========================================================================
         Return Problem's Starts.
        ========================================================================
        """
        return self._starts
