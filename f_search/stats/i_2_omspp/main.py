from f_search.stats import StatsSPP
from f_search.ds import State


class StatsOMSPP(StatsSPP):
    """
    ============================================================================
     Stats for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsSPP.__init__(self)
        self._stats_spp: dict[State, StatsSPP] = dict()

    def fill(self, stats_spp: dict[State, StatsSPP]) -> None:
        """
        ========================================================================
         Fill the Stats with the given StatsSPP.
        ========================================================================
        """
        self._stats_spp = stats_spp
        self.generated = sum(stats.generated for stats in stats_spp.values())
        self.updated = sum(stats.updated for stats in stats_spp.values())
        self.explored = sum(stats.explored for stats in stats_spp.values())

    def __getitem__(self, key: State) -> StatsSPP:
        """
        ========================================================================
         Return the Stats for the given State.
        ========================================================================
        """
        return self._stats_spp[key]
 