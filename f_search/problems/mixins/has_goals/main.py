from f_search.ds.state import StateCell as State


class HasGoals:
    """
    ============================================================================
     Mixin for Problems with multiple Goals.
    ============================================================================
    """

    RECORD_SPEC = {'goals': lambda o: len(o.goals)}

    def __init__(self,
                 goals: list[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals: list[State] = goals
        for i, goal in enumerate(self._goals, start=1):
            goal.name = f'Goal_{i}'

    @property
    def goals(self) -> list[State]:
        """
        ========================================================================
         Return Problem's Goals.
        ========================================================================
        """
        return self._goals
