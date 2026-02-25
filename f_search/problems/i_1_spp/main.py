from f_search.problems import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_search.problems.mixins import HasStart, HasGoal
from typing import Self


class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem on a Grid.
    ============================================================================
    """
    
    # Factory
    Factory = None

    def __init__(self,
                 grid: Grid | str,
                 start: State,
                 goal: State,
                 name: str = 'ProblemSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)

    def reverse(self, name: str = None) -> Self:
        """
        ========================================================================
         Return a reversed Problem (Start and Goal swapped).
        ========================================================================
        """
        name = name if name else self.name
        return type(self)(grid=self.grid,
                          start=self.goal,
                          goal=self.start,
                          name=name)

    def to_light(self) -> Self:
        """
        ========================================================================
         Return a light object (Grid.Name instead of Grid object).
        ========================================================================
        """
        return type(self)(grid=self.grid.name,
                          start=self.start,
                          goal=self.goal,
                          name=self.name)

    def to_heavy(self, grids: dict[str, Grid]) -> Self:
        """
        ========================================================================
         Return a heavy object (Grid object instead of Grid.Name).
        ========================================================================
        """
        return type(self)(grid=grids[self.grid],
                          start=self.start,
                          goal=self.goal,
                          name=self.name)
