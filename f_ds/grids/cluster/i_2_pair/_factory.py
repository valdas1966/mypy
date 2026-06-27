from f_ds.grids import GridMap as Grid, ClusterDiamond as Cluster
from f_ds.grids.cluster.i_2_pair.main import PairCluster


class Factory:
    """
    ============================================================================
     Factory-Class for PairCluster.
    ============================================================================
    """

    @staticmethod
    def diamonds() -> PairCluster:
        """
        ========================================================================
         Return a PairCluster of two deterministic ClusterDiamonds on a
         10x10 GridMap (centers (2,2) and (7,7), steps=2).
        ========================================================================
        """
        grid = Grid(rows=10, cols=10)
        cluster_a = Cluster(grid=grid, center=grid[2][2], steps=2)
        cluster_b = Cluster(grid=grid, center=grid[7][7], steps=2)
        return PairCluster(cluster_a=cluster_a, cluster_b=cluster_b)
