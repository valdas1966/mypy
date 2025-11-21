from f_search.stats import StatsSPP
from f_search.ds import StateBase


class StatsOMSPP(StatsSPP):
    """
    ============================================================================
     Stats for One-to-Many Shortest-Path-Problem.
     Aggregates statistics from multiple SPP sub-problems.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
         Initializes with empty stats, ready to accumulate sub-problem stats.
        ========================================================================
        """
        StatsSPP.__init__(self)
        self._stats_goal: dict[StateBase, StatsSPP] = {}

    def add_goal(self, goal: StateBase, stats: StatsSPP) -> None:
        """
        ========================================================================
         Add stats for a completed goal.
         Updates aggregate counts progressively.
        ========================================================================
        """
        self._stats_goal[goal] = stats
        self.generated += stats.generated
        self.explored += stats.explored

    def __getitem__(self, goal: StateBase) -> StatsSPP:
        """
        ========================================================================
         Return the Stats for the given Goal.
        ========================================================================
        """
        return self._stats_goal[goal]

    @property
    def goals_completed(self) -> int:
        """
        ========================================================================
         Return number of goals that have been reached.
        ========================================================================
        """
        return len(self._stats_goal)
 
    def __repr__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the StatsOMSPP.
        ========================================================================
        """
        return f'StatsOMSPP(elapsed={self.elapsed}, \
                            generated={self.generated}, \
                            explored={self.explored})'
                    