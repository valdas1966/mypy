import pytest

from f_ds.grids.cluster.i_1_diamond.main import ClusterDiamond
from f_ds.grids.grid.map.main import GridMap


def test_a_canonical() -> None:
    """
    ============================================================================
     Canonical Factory.a() returns a 5-cell cluster.
    ============================================================================
    """
    cluster = ClusterDiamond.Factory.a()
    assert len(cluster) == 5


def test_at_center_s1() -> None:
    """
    ============================================================================
     Diamond of steps=1 on a 10x10 no-walls grid has 5 cells.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[5][5], steps=1)
    assert len(cluster) == 5


def test_at_center_s2() -> None:
    """
    ============================================================================
     Diamond of steps=2 on a 10x10 no-walls grid has 13 cells.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[5][5], steps=2)
    assert len(cluster) == 13


def test_at_center_s3() -> None:
    """
    ============================================================================
     Diamond of steps=3 on a 10x10 no-walls grid has 25 cells.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[5][5], steps=3)
    assert len(cluster) == 25


def test_center_and_steps() -> None:
    """
    ============================================================================
     Check the center and steps properties.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    center = grid[2][2]
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=center, steps=1)
    assert cluster.center is center
    assert cluster.steps == 1


def test_contains() -> None:
    """
    ============================================================================
     Cells inside the diamond are members; cells outside are not.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    assert grid[2][2] in cluster
    assert grid[2][3] in cluster
    assert grid[0][0] not in cluster


def test_iteration() -> None:
    """
    ============================================================================
     Iteration produces exactly n_cells items.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    items = list(cluster)
    assert len(items) == 5


def test_key() -> None:
    """
    ============================================================================
     The key is (center.key, steps).
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    assert cluster.key == ((2, 2), 1)


def test_walls_excluded() -> None:
    """
    ============================================================================
     Wall cells are skipped by BFS construction.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    grid.invalidate([grid[2][3]])
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    assert len(cluster) == 4
    assert grid[2][3] not in cluster


def test_random_meets_min() -> None:
    """
    ============================================================================
     Factory.random returns a cluster of at least min_cells cells.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    cluster = ClusterDiamond.Factory.random(
        grid=grid, min_cells=8, steps=2)
    assert len(cluster) >= 8


def test_random_raises_when_impossible() -> None:
    """
    ============================================================================
     Factory.random raises ValueError if min_cells is unreachable.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    with pytest.raises(ValueError):
        ClusterDiamond.Factory.random(
            grid=grid, min_cells=1000, steps=1, max_tries=10)


def test_bool_truthy() -> None:
    """
    ============================================================================
     A cluster with cells is truthy.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    assert bool(cluster) is True


def test_str() -> None:
    """
    ============================================================================
     __str__ produces the expected format.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    cluster = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[2][2], steps=1)
    s = str(cluster)
    assert 'ClusterDiamond' in s
    assert '(2, 2)' in s
    assert 'steps=1' in s
    assert 'cells=5' in s
