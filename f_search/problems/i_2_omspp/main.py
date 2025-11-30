from f_search.problems import ProblemSearch, Grid, State
from f_search.problems.i_1_spp.main import ProblemSPP
from f_search.problems.mixins import HasStart, HasGoals


class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    """
    ============================================================================
     One-to-Many Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 grid: Grid,
                 start: State,
                 goals: list[State],
                 name: str = 'ProblemOMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)

    def to_spps(self) -> list[ProblemSPP]:
        """
        ========================================================================
         Convert the ProblemOMSPP to a list of ProblemSPPs.
        ========================================================================
        """
        sub_problems: list[ProblemSPP] = []
        for goal in self.goals:
            sub_problem = ProblemSPP(grid=self.grid,
                                       start=self.start,
                                       goal=goal)
            sub_problems.append(sub_problem)
        return sub_problems
    
    def __str__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the ProblemOMSPP.
        ========================================================================
        """
        return f'{self.name}(Grid={str(self.grid)}, Start={str(self.start)}, #Goals={len(self.goals)})   '

    