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
                 sub_solutions: dict[State, SolutionOOSPP]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        elapsed_per_goal = {goal: sub_solution.stats.elapsed
                            for goal, sub_solution
                            in sub_solutions.items()}
        generated_per_goal = {goal: sub_solution.stats.generated
                             for goal, sub_solution
                             in sub_solutions.items()}
        updated_per_goal = {goal: sub_solution.stats.updated
                            for goal, sub_solution
                            in sub_solutions.items()}
        explored_per_goal = {goal: sub_solution.stats.explored
                             for goal, sub_solution
                             in sub_solutions.items()}
        stats = StatsOMSPP(elapsed_per_goal=elapsed_per_goal,
                           generated_per_goal=generated_per_goal,
                           updated_per_goal=updated_per_goal,
                           explored_per_goal=explored_per_goal)
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
