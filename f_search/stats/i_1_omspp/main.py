from f_search.stats.i_0_base.main import StatsSearch
from f_search.ds.state import State


class StatsOMSPP(StatsSearch):
    """
    ============================================================================
     Stats for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 elapsed_per_goal: dict[State, float],
                 generated_per_goal: dict[State, int],
                 updated_per_goal: dict[State, int],
                 explored_per_goal: dict[State, int]
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        elapsed = sum(elapsed_per_goal.values())
        generated = sum(generated_per_goal.values())
        updated = sum(updated_per_goal.values())
        explored = sum(explored_per_goal.values())
        StatsSearch.__init__(self,
                             elapsed=elapsed,
                             updated=updated,
                             generated=generated,
                             explored=explored)
        self._generated_per_goal = generated_per_goal
        self._updated_per_goal = updated_per_goal
        self._explored_per_goal = explored_per_goal
        self._elapsed_per_goal = elapsed_per_goal

    @property
    def generated_per_goal(self) -> dict[State, int]:
        """
        ========================================================================
         Return the Number of Generated Nodes for Each Goal.
        ========================================================================
        """
        return self._generated_per_goal

    @property
    def explored_per_goal(self) -> dict[State, int]:
        """
        ========================================================================
         Return the Number of Explored Nodes for Each Goal.
        ========================================================================
        """
        return self._explored_per_goal

    @property
    def elapsed_per_goal(self) -> dict[State, float]:
        """
        ========================================================================
         Return the Elapsed Seconds for Each Sub-Search (Goal).
        ========================================================================
        """
        return self._elapsed_per_goal
