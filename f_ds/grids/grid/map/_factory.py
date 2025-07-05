from f_ds.grids.grid.map.main import GridMap


class FactoryGridMap:
    """
    ============================================================================
     Factory for the GridMap.
    ============================================================================
    """

    @staticmethod
    def x() -> GridMap:
        """
        ========================================================================
         Return a GridMap with 3 rows and 3 columns in a X-Shape.
        ========================================================================
        """
        grid = GridMap(rows=3)
        grid[0][1].set_invalid()
        grid[1][0].set_invalid()
        grid[1][2].set_invalid()
        grid[2][1].set_invalid()
        return grid
    