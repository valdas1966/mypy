from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.problems import ProblemSPP as Problem
from f_search.stats import StatsSearch
from f_search.ds.path import Path


class SolutionSPP(SolutionSearch[Problem, StatsSearch]):
    """
    ============================================================================
     Solution for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 name_algo: str,
                 problem: Problem,
                 is_valid: bool,
                 path: Path = None,
                 g_goal: int = None,
                 stats: StatsSearch = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        stats = stats if stats else StatsSearch()
        SolutionSearch.__init__(self,
                                name_algo=name_algo,
                                problem=problem,
                                is_valid=is_valid,
                                stats=stats)
        self._path = path
        self._g_goal = g_goal

    @property
    def path(self) -> Path:
        """
        ========================================================================
         Return the Solution's Path.
        ========================================================================
        """
        return self._path

    @property
    def g_goal(self) -> int | None:
        """
        ========================================================================
         Return the optimal cost to reach the Goal.
        ========================================================================
        """
        return self._g_goal

    @property
    def quality_h(self) -> float | None:
        """
        ========================================================================
         Return Heuristic Quality as h(start) / g(goal) in [0, 1].
        ========================================================================
        """
        if not self or not self._g_goal:
            return None
        return self.problem.h_start / self._g_goal

    @property
    def efficiency(self) -> float | None:
        """
        ========================================================================
         Return Search Efficiency as len(path) / explored.
        ========================================================================
        """
        if not self or not self.stats.explored:
            return None
        if self._path:
            return len(self._path) / self.stats.explored
        if self._g_goal is not None:
            return (self._g_goal + 1) / self.stats.explored
        return None
