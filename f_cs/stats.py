from abc import ABC


class StatsAlgo(ABC):
    """
    ============================================================================
     ABC for Algorithm's Stats.
    ============================================================================
    """
    def __init__(self, elapsed: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._elapsed: int = elapsed

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the Elapsed seconds for Algorithm to reach the Solution.
        ========================================================================
        """
        return self._elapsed
