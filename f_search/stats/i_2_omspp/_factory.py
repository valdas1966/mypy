from f_search.stats.i_2_omspp.main import StatsOMSPP, StatsSPP, State


class Factory:
    """
    ============================================================================
     Factory for the StatsOMSPP.
    ============================================================================
    """

    @staticmethod
    def ab() -> StatsOMSPP:
        """
        ========================================================================
         Return a StatsOMSPP with all values set to 10.
        ========================================================================
        """
        stats_a = StatsSPP.Factory.a()
        stats_b = StatsSPP.Factory.b()
        state_a = State.Factory.a()
        state_b = State.Factory.b()
        stats_spp = {state_a: stats_a,
                     state_b: stats_b}
        stats = StatsOMSPP()
        stats.fill(stats_spp=stats_spp)
        return stats
