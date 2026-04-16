from f_hs.problem.i_1_grid.main import ProblemGrid
from f_ds.grids.grid.map import GridMap


class Factory:
    """
    ========================================================================
     Factory for ProblemGrid test instances.
    ========================================================================
    """

    @staticmethod
    def grid_3x3() -> ProblemGrid:
        """
        ====================================================================
         Open 3x3 Grid: (0,0) -> (2,2), cost 4.
        ====================================================================
        """
        grid = GridMap(rows=3, cols=3)
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[2][2])

    @staticmethod
    def grid_3x3_obstacle() -> ProblemGrid:
        """
        ====================================================================
         3x3 Grid with obstacle at (1,1): (0,0) -> (2,2).
        ====================================================================
        """
        grid = GridMap(rows=3, cols=3)
        grid[1][1].set_invalid()
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[2][2])

    @staticmethod
    def grid_4x4_obstacle() -> ProblemGrid:
        """
        ====================================================================
         4x4 Grid with a vertical 2-cell wall at (0,2) and (1,2).
         Start (0,0), Goal (0,3). The wall forces a detour through
         row 2 — optimal cost is 7 (vs. 3 without obstacles).
        ====================================================================
        """
        grid = GridMap(rows=4)
        grid[0][2].set_invalid()
        grid[1][2].set_invalid()
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[0][3])

    @staticmethod
    def grid_3x3_no_path() -> ProblemGrid:
        """
        ====================================================================
         3x3 Grid with wall blocking all paths: (0,0) -> (2,2).
        ====================================================================
        """
        grid = GridMap(rows=3, cols=3)
        # Block the middle row
        grid[1][0].set_invalid()
        grid[1][1].set_invalid()
        grid[1][2].set_invalid()
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[2][2])

    @staticmethod
    def grid_3x3_start_is_goal() -> ProblemGrid:
        """
        ====================================================================
         3x3 Grid where start equals goal: (0,0).
        ====================================================================
        """
        grid = GridMap(rows=3, cols=3)
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[0][0])
