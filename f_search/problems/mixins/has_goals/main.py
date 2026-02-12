from f_search.ds.state import StateCell as State


class HasGoals:
    """
    ============================================================================
     Mixin for Problems with multiple Goals.
    ============================================================================
    """

    def __init__(self,
                 goals: list[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals: list[State] = goals

    @property
    def goals(self) -> list[State]:
        """
        ========================================================================
         Return Problem's Goals.
        ========================================================================
        """
        return self._goals
