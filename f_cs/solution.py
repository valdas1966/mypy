from f_cs.stats import StatsAlgo    
from f_core.mixins.validatable_public import ValidatablePublic
from typing import Generic, TypeVar

Stats = TypeVar('Stats', bound=StatsAlgo)


class SolutionAlgo(Generic[Stats], ValidatablePublic):
    """
    ============================================================================
     ABC for Algorithm's Solution.
    ============================================================================
    """
    def __init__(self,
                  is_valid: bool,
                    stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ValidatablePublic.__init__(self, is_valid=is_valid)
        self._stats: Stats = stats

    @property
    def stats(self) -> Stats:
        """
        ========================================================================
         Return the Algorithm's Stats.
        ========================================================================
        """
        return self._stats
