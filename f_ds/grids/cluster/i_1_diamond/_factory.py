from f_ds.grids import (GridMap as Grid,
                        CellMap as Cell,
                        ClusterDiamond as Cluster)


class Factory:
    """
    ============================================================================
     Factory-Class for ClusterDiamond.
    ============================================================================
    """

    @staticmethod
    def random(grid: Grid,
               min_cells: int,
               steps: int,
               max_tries: int = 100) -> Cluster:
        """
        ========================================================================
         Sample a ClusterDiamond around a random valid center.
         Retries until the cluster has >= min_cells cells.
         Raises ValueError after max_tries.
        ========================================================================
        """
        for _ in range(max_tries):
            center = grid.random.cells(size=1)[0]
            cluster = Cluster(grid=grid,
                              center=center,
                              steps=steps)
            if len(cluster) >= min_cells:
                return cluster
        raise ValueError(
            f'Could not sample a ClusterDiamond with '
            f'>= {min_cells} valid cells after '
            f'{max_tries} tries.')

    @staticmethod
    def random_many(grid: Grid,
                    many: int,
                    steps: int,
                    min_cells: int = 1,
                    max_tries: int = 100) -> list[Cluster]:
        """
        ========================================================================
         1. Return many distinct random Clusters
         2. Raises ValueError if the distinct target cannot be reached.
        ========================================================================
        """
        clusters: set[Cluster] = set()
        tries = many * max_tries
        while len(clusters) < many and tries:
            cluster = Factory.random(grid, min_cells, steps, max_tries)
            clusters.add(cluster)
            tries -= 1
        if len(clusters) < many:
            raise ValueError(
                f'Could only sample {len(clusters)} distinct '
                f'ClusterDiamonds of {many} requested '
                f'(min_cells={min_cells}, steps={steps}) within '
                f'{many * max_tries} tries.')
        return list(clusters)
