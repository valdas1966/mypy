import pytest

from f_ds.grids import GridMap as Grid, ClusterDiamond as Cluster


def test_center_full() -> None:
    """
    ============================================================================
     Diamond of steps=1 on a 10x10 no-walls grid has 5 cells.
    ============================================================================
    """
    grid = Grid(rows=3)
    center = grid[1][1]
    cluster = Cluster(grid=grid, center=center, steps=1)
    assert len(cluster) == 5
    assert str(cluster) == 'ClusterDiamond(center=(1, 1), steps=1, cells=5)'
    assert repr(cluster) == '<ClusterDiamond: ClusterDiamond(center=(1, 1), steps=1, cells=5)>'


def test_center_part() -> None:
    """
    ============================================================================
     Diamond of steps=1 on a 10x10 no-walls grid has 5 cells.
    ============================================================================
    """
    grid = Grid(rows=3)
    center = grid[0][0]
    cluster = Cluster(grid=grid, center=center, steps=1)
    assert len(cluster) == 3


def test_key() -> None:
    """
    ============================================================================
     The key is (map_name, center.key, steps).
    ============================================================================
    """
    grid = Grid(name='test', rows=3)
    center = grid[1][1]
    cluster = Cluster(grid=grid, center=center, steps=1)
    assert cluster.key == ('test', (1, 1), 1)


def test_random_many_distinct() -> None:
    """
    ============================================================================
     random_many returns exactly `many` DISTINCT diamonds.
    ============================================================================
    """
    grid = Grid(rows=10)
    clusters = Cluster.Factory.random_many(grid=grid, many=6, steps=1)
    assert len(clusters) == 6
    assert len(set(clusters)) == 6
    assert all(isinstance(c, Cluster) for c in clusters)


def test_random_many_raises_when_infeasible() -> None:
    """
    ============================================================================
     random_many raises when `many` exceeds the distinct clusters available.
    ============================================================================
    """
    grid = Grid(rows=2)        # 4 valid cells -> at most 4 distinct diamonds
    with pytest.raises(ValueError):
        Cluster.Factory.random_many(grid=grid, many=99, steps=1)
