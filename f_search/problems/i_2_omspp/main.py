from f_search.problems import ProblemSearch
from f_search.problems.i_1_spp.main import ProblemSPP
from f_search.problems.mixins import HasStart, HasGoals
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from typing import Self


class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    """
    ============================================================================
     One-to-Many Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 grid: Grid | str,
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

    def to_light(self) -> Self:
        """
        ========================================================================
         Return a light object (Grid.Name instead of Grid object).
        ========================================================================
        """
        return type(self)(grid=self.grid.name,
                          start=self.start,
                          goals=self.goals,
                          name=self.name)

    def to_heavy(self, grids: dict[str, Grid]) -> Self:
        """
        ========================================================================
         Return a heavy object (Grid object instead of Grid.Name).
        ========================================================================
        """
        return type(self)(grid=grids[self.grid],
                          start=self.start,
                          goals=self.goals,
                          name=self.name)
