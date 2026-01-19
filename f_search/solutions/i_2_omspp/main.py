from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.solutions.i_1_spp.main import SolutionSPP
from f_search.stats import StatsSearch
from f_search.ds.path import Path
from f_search.ds.states import StateBase as State


class SolutionOMSPP(SolutionSearch[StatsSearch]):
    """
    ============================================================================
     Solution for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    def __init__(self,
                 sub_solutions: dict[State, SolutionSPP],
                 elapsed: int) -> None:
        """
        ========================================================================
         Init private Attributes.
         Stats are already accumulated by the algorithm during execution.
        ========================================================================
        """
        generated = sum(sub_solution.stats.generated
                        for sub_solution
                        in sub_solutions.values())
        explored = sum(sub_solution.stats.explored
                       for sub_solution
                       in sub_solutions.values())
        is_valid = all(sub_solution
                       for sub_solution
                       in sub_solutions.values())
        stats = StatsSearch(elapsed=elapsed,
                            generated=generated,
                            explored=explored)
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._sub_solutions = sub_solutions
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

    @property
    def subs(self) -> dict[State, SolutionSPP]:
        """
        ========================================================================
         Return the Sub-Solutions.
        ========================================================================
        """
        return self._sub_solutions
