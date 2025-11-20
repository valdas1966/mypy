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
         Return a StatsOMSPP with stats for goals A and B.
        ========================================================================
        """
        stats_a = StatsSPP.Factory.a()
        stats_b = StatsSPP.Factory.b()
        state_a = State.Factory.a()
        state_b = State.Factory.b()
        stats = StatsOMSPP()
        stats.add_stats_goal(goal=state_a, stats=stats_a)
        stats.add_stats_goal(goal=state_b, stats=stats_b)
        return stats
