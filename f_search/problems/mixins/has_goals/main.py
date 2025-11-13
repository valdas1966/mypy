from f_search.ds import State
from typing import Iterable


class HasGoals:
    """
    ============================================================================
     Mixin for Problems with Goals.
    ============================================================================
    """

    def __init__(self,
                 goals: Iterable[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals: set[State] = set(goals)

    @property
    def goals(self) -> set[State]:
        """
        ========================================================================
         Return Problem's Goals.
        ========================================================================
        """
        return self._goals
