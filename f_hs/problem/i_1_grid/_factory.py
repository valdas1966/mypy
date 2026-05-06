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
         Canonical OOSPP test instance — 4x4 grid with a
         vertical 2-cell wall at (0,2) and (1,2). Start (0,0),
         goal (0,3). The wall forces a detour through row 2;
         optimal cost is 7 (vs. 3 without obstacles).

         Used as the cross-algorithm OOSPP benchmark by every
         AStar-family tester (AStar, AStarLookup, Dijkstra,
         BFS) and by OOSPP scripts.
         The OMSPP twin is `grid_4x4_obstacle_omspp()` (same
         grid, multi-goal).
        ====================================================================
        """
        grid = GridMap(rows=4)
        grid[0][2].set_invalid()
        grid[1][2].set_invalid()
        return ProblemGrid(grid=grid,
                           start=grid[0][0],
                           goal=grid[0][3])

    @staticmethod
    def grid_4x4_obstacle_omspp() -> ProblemGrid:
        """
        ====================================================================
         Canonical OMSPP test instance — `grid_4x4_obstacle`
         with start (0,0) and the three "far corner" goals:
         (0,3), (3,0), (3,3).

         Optimal costs from the start to each goal:
           (0,3) = 7   — obstacle blocks the direct east route;
                         must detour south through row 2.
           (3,0) = 3   — straight south down column 0.
           (3,3) = 6   — moderate route around the obstacle.

         Cost spread {3, 6, 7} + directional spread (E / S / SE)
         give MIN / MAX / AVG / RND / PROJECTION aggregation
         operators visibly different f-trajectories per state,
         which is the whole point of an OMSPP benchmark — the
         operators must be distinguishable for the tests to
         have signal.

         Inter-sub-search reuse opportunities:
           - paths to (0,3) and (3,3) share the south-through-
             row-2 prefix (KAStarInc benefits).
           - path to (3,0) goes straight down column 0,
             diverging early (low reuse — by design, exercises
             the case where caching doesn't help).

         Used as the cross-algorithm benchmark by every OMSPP
         tester and script (canonical anchor for cross-algo
         counter / recording comparison). Per-algo edge-case
         scenarios (unreachable goal, duplicate goals, k=1,
         start==goal, weighted edges, inconsistent h) stay
         local to their tester.
        ====================================================================
        """
        grid = GridMap(rows=4)
        grid[0][2].set_invalid()
        grid[1][2].set_invalid()
        return ProblemGrid(
            grid=grid,
            starts=[grid[0][0]],
            goals=[grid[0][3], grid[3][0], grid[3][3]],
        )

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
