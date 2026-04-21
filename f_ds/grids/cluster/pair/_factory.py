from f_ds.grids.cluster.pair.main import PairCluster
from f_ds.grids.cluster.i_1_diamond.main import ClusterDiamond
from f_ds.grids.grid.map.main import GridMap


class Factory:
    """
    ============================================================================
     Factory-Class for PairCluster.
    ============================================================================
    """

    @staticmethod
    def of_diamonds(grid: GridMap,
                    center_a,
                    center_b,
                    steps: int
                    ) -> PairCluster[ClusterDiamond]:
        """
        ========================================================================
         Return a PairCluster of two ClusterDiamonds at the given centers.
        ========================================================================
        """
        a = ClusterDiamond.Factory.at_center(
            grid=grid, center=center_a, steps=steps)
        b = ClusterDiamond.Factory.at_center(
            grid=grid, center=center_b, steps=steps)
        return PairCluster(a=a, b=b)

    @staticmethod
    def random(grid: GridMap,
               min_cells_a: int,
               min_cells_b: int,
               steps: int,
               min_distance: int,
               max_tries: int = 100
               ) -> PairCluster[ClusterDiamond]:
        """
        ========================================================================
         Sample two disjoint ClusterDiamonds on the grid such that:
           (a) len(A) >= min_cells_a and len(B) >= min_cells_b,
           (b) dist(A.center, B.center) >= min_distance,
           (c) A and B share no cells.
         Raises ValueError after max_tries.
        ========================================================================
        """
        for _ in range(max_tries):
            a = ClusterDiamond.Factory.random(
                grid=grid,
                min_cells=min_cells_a,
                steps=steps)
            b = ClusterDiamond.Factory.random(
                grid=grid,
                min_cells=min_cells_b,
                steps=steps)
            # Check center distance
            if a.center.distance(other=b.center) < min_distance:
                continue
            # Check disjoint cells
            a_keys = {cell.key for cell in a}
            b_keys = {cell.key for cell in b}
            if a_keys & b_keys:
                continue
            return PairCluster(a=a, b=b)
        raise ValueError(
            f'Could not sample a disjoint PairCluster with '
            f'min_cells_a={min_cells_a}, '
            f'min_cells_b={min_cells_b}, steps={steps}, '
            f'min_distance={min_distance} after '
            f'{max_tries} tries.')

    @staticmethod
    def a() -> PairCluster[ClusterDiamond]:
        """
        ========================================================================
         Canonical small PairCluster for testing.
         8x8 grid, two non-overlapping diamonds at (1,1) and (6,6),
         steps=1 each; center-distance = 10.
        ========================================================================
        """
        grid = GridMap(rows=8, cols=8)
        return Factory.of_diamonds(grid=grid,
                                   center_a=grid[1][1],
                                   center_b=grid[6][6],
                                   steps=1)
