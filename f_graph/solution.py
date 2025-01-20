from f_cs.solution import SolutionAlgo, StatsAlgo
from typing import TypeVar, Generic

Stats = TypeVar('Stats', bound=StatsAlgo)


class SolutionGraph(Generic[Stats], SolutionAlgo[Stats]):
    """
    ============================================================================
     ABC for Solution of Graph-Problem.
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
        SolutionAlgo.__init__(self, is_valid=is_valid, stats=stats)
