from f_search.stats.i_0_base.main import StatsSearch


class StatsSPP(StatsSearch):
    """
    ============================================================================
     Stats for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    
    # Factory
    Factory: type = None

    def __init__(self, name: str = 'StatsSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsSearch.__init__(self, name=name)

    def __str__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the StatsSPP.
        ========================================================================
        """
        return f'{self.name}[Generated={self.generated}, Explored={self.explored}]'
    