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

    @staticmethod
    def _sample_pool(grid: Grid,
                     many: int,
                     steps: int,
                     min_cells: int,
                     max_tries: int) -> list[Cluster]:
        """
        ========================================================================
         Best-effort pool of up to `many` DISTINCT ClusterDiamonds on `grid`
         (radius `steps`, each with >= `min_cells` cells). A grid that cannot
         supply `many` distinct diamonds within its try budget yields fewer
         and returns what it has -- no raise (graceful on sparse mazes /
         large min_cells). De-duplication is by ClusterDiamond identity.
        ========================================================================
        """
        pool: set[Cluster] = set()
        tries = many * max_tries
        while len(pool) < many and tries > 0:
            try:
                pool.add(Cluster.Factory.random(grid=grid,
                                                min_cells=min_cells,
                                                steps=steps,
                                                max_tries=max_tries))
            except ValueError:
                break
            tries -= 1
        return list(pool)

    @staticmethod
    def random_many(grid: Grid,
                    many: int,
                    steps_a: int = 0,
                    min_cells_a: int = 1,
                    steps_b: int = 1,
                    min_cells_b: int = 1,
                    min_dist: int = 0,
                    max_tries: int = 100) -> list[PairCluster]:
        """
        ========================================================================
         Sample two pools of DISTINCT ClusterDiamonds on `grid` -- up to
         `many` "A" diamonds (steps_a / min_cells_a) and up to `many` "B"
         diamonds (steps_b / min_cells_b) -- and return every
         PairCluster(a, b) whose center-to-center distance() >= `min_dist`
         (the full A x B cross product, so up to many*many pairs).

         Sampling is best-effort: a grid that cannot supply `many` distinct
         diamonds of a side yields fewer, so coverage degrades gracefully
         instead of raising. `min_dist=0` (default) keeps every pair.

         Randomness is the PROCESS-GLOBAL `random` module (each draw goes
         through ClusterDiamond.Factory.random -> grid.random.cells); seed
         it before calling for a reproducible pool. `max_tries` bounds the
         per-diamond center resampling on both sides.
        ========================================================================
        """
        pool_a = Factory._sample_pool(grid=grid,
                                      many=many,
                                      steps=steps_a,
                                      min_cells=min_cells_a,
                                      max_tries=max_tries)
        pool_b = Factory._sample_pool(grid=grid,
                                      many=many,
                                      steps=steps_b,
                                      min_cells=min_cells_b,
                                      max_tries=max_tries)
        pairs: list[PairCluster] = []
        for a in pool_a:
            for b in pool_b:
                pair = PairCluster(cluster_a=a, cluster_b=b)
                if pair.distance() >= min_dist:
                    pairs.append(pair)
        return pairs
