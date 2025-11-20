from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.solutions.i_1_spp.main import SolutionSPP
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
                 sub_solutions: dict[State, SolutionSPP]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        stats_spp = {goal: sub_solution.stats
                     for goal, sub_solution
                     in sub_solutions.items()}
        stats.fill(stats_spp=stats_spp)
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._paths = {goal: sub_solution.path
                       for goal, sub_solution
                       in sub_solutions.items()}

    @property
    def paths(self) -> dict[State, Path]:
        """
        ========================================================================
         Return the Solution's Paths for Each Goal.
        ========================================================================
        """
        return self._paths
