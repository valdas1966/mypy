from f_search.ds.states import StateCell as State


class HasGoal:
    """
    ============================================================================
     Mixin-Class for Problems with a Goal-State.
    ============================================================================
    """

    def __init__(self, goal: State) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal   
        self._goal.name = 'Goal'

    @property
    def goal(self) -> State:
        """
        ========================================================================
         Return the Goal-State of the Problem.
        ========================================================================
        """
        return self._goal
