from f_core.mixins.printable import Printable
from f_cs.stats.main import StatsAlgo


class StatsPath(StatsAlgo, Printable):
    """
    ============================================================================
     Stats for Path-Graphs.
    ============================================================================
    """

    def __init__(self,
                 elapsed: int = 0,
                 generated: int = 0,
                 explored: int = 0,
                 changed: dict[int, int] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self, elapsed=elapsed)
        self._generated: int = generated
        self._explored: int = explored

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the Number of Generated-Nodes.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the Number of Explored-Nodes.
        ========================================================================
        """
        return self._explored
    
    def __str__(self) -> str:
        """
        ========================================================================
         Return the String Representation of the Stats.
        ========================================================================
        """
        return f'Elapsed={self._elapsed}, Generated={self._generated}, Explored={self._explored}'
