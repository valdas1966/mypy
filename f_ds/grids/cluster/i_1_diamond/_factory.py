from f_ds.grids.cluster.i_1_diamond.main import ClusterDiamond
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class Factory:
    """
    ============================================================================
     Factory-Class for ClusterDiamond.
    ============================================================================
    """

    @staticmethod
    def at_center(grid: GridMap,
                  center: CellMap,
                  steps: int) -> ClusterDiamond:
        """
        ========================================================================
         Return a ClusterDiamond centered at the given cell.
        ========================================================================
        """
        return ClusterDiamond(grid=grid,
                              center=center,
                              steps=steps)

    @staticmethod
    def random(grid: GridMap,
               min_cells: int,
               steps: int,
               max_tries: int = 100) -> ClusterDiamond:
        """
        ========================================================================
         Sample a ClusterDiamond around a random valid center.
         Retries until the cluster has >= min_cells cells.
         Raises ValueError after max_tries.
        ========================================================================
        """
        for _ in range(max_tries):
            center = grid.random.cells(size=1)[0]
            cluster = ClusterDiamond(grid=grid,
                                     center=center,
                                     steps=steps)
            if len(cluster) >= min_cells:
                return cluster
        raise ValueError(
            f'Could not sample a ClusterDiamond with '
            f'>= {min_cells} valid cells after '
            f'{max_tries} tries.')

    @staticmethod
    def a() -> ClusterDiamond:
        """
        ========================================================================
         Canonical small ClusterDiamond for testing.
         4x4 no-walls grid, center at (1,1), steps=1 => 5 cells.
        ========================================================================
        """
        grid = GridMap.Factory.four_without_obstacles()
        return ClusterDiamond(grid=grid,
                              center=grid[1][1],
                              steps=1)
