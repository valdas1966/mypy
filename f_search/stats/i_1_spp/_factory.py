from f_search.stats.i_1_spp.main import StatsSPP


class Factory:
    """
    ============================================================================
     Factory for the StatsSPP.
    ============================================================================
    """

    @staticmethod
    def a() -> StatsSPP:
        """
        ========================================================================
         Return a StatsSPP with all values set to 10.
        ========================================================================
        """
        stats = StatsSPP()
        stats.elapsed = 10
        stats.generated = 10
        stats.updated = 10
        stats.explored = 10
        return stats

    @staticmethod
    def b() -> StatsSPP:
        """
        ========================================================================
         Return a StatsSPP with all values set to 20.
        ========================================================================
        """
        stats = StatsSPP()
        stats.elapsed = 20
        stats.generated = 20
        stats.updated = 20
        stats.explored = 20
        return stats
