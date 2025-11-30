from f_core.mixins.validatable_public import ValidatablePublic
from f_core.mixins.has.record import HasRecord
from f_cs.stats import StatsAlgo
from typing import Generic, TypeVar

Stats = TypeVar('Stats', bound=StatsAlgo)


class SolutionAlgo(Generic[Stats], ValidatablePublic, HasRecord):
    """
    ============================================================================
     ABC for Algorithm's Solution.
    ============================================================================
    """

    RECORD_SPEC = {'is_valid': lambda o: bool(o),
                   'stats': lambda o: o.stats.record}

    def __init__(self,
                 is_valid: bool,
                 stats: Stats,
                 name: str = 'SolutionAlgo') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ValidatablePublic.__init__(self, is_valid=is_valid)
        HasRecord.__init__(self, name=name)
        self._stats: Stats = stats

    @property
    def stats(self) -> Stats:
        """
        ========================================================================
         Return the Algorithm's Stats.
        ========================================================================
        """
        return self._stats
