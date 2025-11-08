from f_search.problems.i_0_base.main import ProblemSearch, Grid


class Factory:
    """
    ============================================================================
     Factory for the ProblemSearch.
    ============================================================================
    """

    @staticmethod
    def grid_3x3() -> ProblemSearch:
        """
        ========================================================================
         Return a ProblemSearch object with a 3x3 grid.
        ========================================================================
        """
        class Temp(ProblemSearch):
            def __init__(self) -> None:
                grid = Grid(rows=3)
                ProblemSearch.__init__(self, grid=grid)
        return Temp()
