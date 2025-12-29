from f_search.problems import ProblemOMSPP, State
from f_ds.grids import GridMap as Grid


class ProblemOMSPPLite:
    """
    ============================================================================
     Light-Weighted (not executable) One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 grid: str,
                 start: State,
                 goals: list[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid
        self._start = start
        self._goals = goals

    def materialize(self, grids: dict[str, Grid]) -> ProblemOMSPP:
        """
        ========================================================================
         Materialize the ProblemOMSPPLight into a ProblemOMSPP.
        ========================================================================
        """
        grid = grids[self._grid]
        return ProblemOMSPP(grid=grid,
                            start=self._start,
                            goals=self._goals)
