from f_search.stats.i_0_base.main import StatsSearch


class StatsSPP(StatsSearch):
    """
    ============================================================================
     Stats for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    
    # Factory
    Factory: type = None

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the StatsSPP.
        ========================================================================
        """
        return f'StatsSPP(elapsed={self.elapsed}, \
                          generated={self.generated}, \
                          explored={self.explored})'
