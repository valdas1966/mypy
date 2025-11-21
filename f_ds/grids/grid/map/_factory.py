from f_ds.grids.grid.map.main import GridMap


class Factory:
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

    @staticmethod
    def four_without_obstacles() -> GridMap:
        """
        ========================================================================
         Return a GridMap with 4 rows and 4 columns without obstacles.
        ========================================================================
        """
        grid = GridMap(rows=4, name='Grid4x4')
        return grid

    @staticmethod
    def four_with_obstacles() -> GridMap:
        """
        ========================================================================
         Return a GridMap with 4 rows and 4 columns with obstacles.
        ========================================================================
        """
        grid = GridMap(rows=4, name='Grid4x4Obstacles')
        grid[0][2].set_invalid()
        grid[1][2].set_invalid()
        return grid
