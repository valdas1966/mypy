from f_search.solutions import SolutionSearch
from f_search.solutions import SolutionSPP
from f_search.problems import ProblemOMSPP
from f_search.stats import StatsSearch
from f_search.ds.path import Path
from f_search.ds.state import StateBase as State


class SolutionOMSPP(SolutionSearch[ProblemOMSPP, StatsSearch]):
    """
    ============================================================================
     Solution for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOMSPP,
                 subs: dict[State, SolutionSPP],
                 elapsed: int) -> None:
        """
        ========================================================================
         Init private Attributes.
         Stats are already accumulated by the algorithm during execution.
        ========================================================================
        """
        discovered = sum(sub_solution.stats.discovered
                         for sub_solution
                         in subs.values())
        explored = sum(sub_solution.stats.explored
                       for sub_solution
                       in subs.values())
        is_valid = all(sub_solution
                       for sub_solution
                       in subs.values())
        stats = StatsSearch(elapsed=elapsed,
                            discovered=discovered,
                            explored=explored)
        SolutionSearch.__init__(self, problem=problem, is_valid=is_valid, stats=stats)
        self._sub_solutions = subs
        self._paths = {goal: sub_solution.path
                       for goal, sub_solution
                       in subs.items()}

    @property
    def paths(self) -> dict[State, Path]:
        """
        ========================================================================
         Return the Solution's Paths for Each Goal.
        ========================================================================
        """
        return self._paths

    @property
    def subs(self) -> dict[State, SolutionSPP]:
        """
        ========================================================================
         Return the Sub-Solutions.
        ========================================================================
        """
        return self._sub_solutions
