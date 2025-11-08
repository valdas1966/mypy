from f_search.problems.mixins.has_grid.main import HasGrid, Grid


class Factory:
    """
    ============================================================================
     Factory for the HasGrid mixin.
    ============================================================================
    """

    @staticmethod
    def grid_3x3() -> HasGrid:
        """
        ========================================================================
         Return a HasGrid object with a 3x3 grid.
        ========================================================================
        """
        class Temp(HasGrid):
            def __init__(self) -> None:
                grid = Grid(rows=3)
                HasGrid.__init__(self, grid=grid)
        return Temp()
