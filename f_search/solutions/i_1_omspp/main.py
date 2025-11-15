from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.solutions.i_1_oospp.main import SolutionOOSPP
from f_search.stats import StatsOMSPP
from f_search.ds.path import Path
from f_search.ds.state import State


class SolutionOMSPP(SolutionSearch[StatsOMSPP]):
    """
    ============================================================================
     Solution for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    def __init__(self,
                 is_valid: bool,
                 stats: StatsOMSPP,
                 paths: dict[State, Path],
                 sub_solutions: dict[State, SolutionOOSPP]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._paths = paths

    @property
    def paths(self) -> dict[State, Path]:
        """
        ========================================================================
         Return the Solution's Paths for Each Goal.
        ========================================================================
        """
        return self._paths
