import pytest

from f_ds.grids.cluster.pair.main import PairCluster
from f_ds.grids.cluster.i_1_diamond.main import ClusterDiamond
from f_ds.grids.grid.map.main import GridMap


def test_a_canonical() -> None:
    """
    ============================================================================
     Canonical Factory.a() returns two diamonds with center-distance 10.
    ============================================================================
    """
    pair = PairCluster.Factory.a()
    assert pair.distance == 10
    assert len(pair.a) == 5
    assert len(pair.b) == 5


def test_distance_manhattan() -> None:
    """
    ============================================================================
     Distance is Manhattan between the two centers.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    a = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[1][1], steps=1)
    b = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[8][8], steps=1)
    pair = PairCluster(a=a, b=b)
    # |1-8| + |1-8| = 14
    assert pair.distance == 14


def test_a_b_properties() -> None:
    """
    ============================================================================
     a and b return the correct clusters.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    a = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[1][1], steps=1)
    b = ClusterDiamond.Factory.at_center(
        grid=grid, center=grid[8][8], steps=1)
    pair = PairCluster(a=a, b=b)
    assert pair.a is a
    assert pair.b is b


def test_of_diamonds_factory() -> None:
    """
    ============================================================================
     Factory.of_diamonds builds a pair of diamonds at given centers.
    ============================================================================
    """
    grid = GridMap(rows=10, cols=10)
    pair = PairCluster.Factory.of_diamonds(
        grid=grid,
        center_a=grid[2][2],
        center_b=grid[7][7],
        steps=2)
    assert pair.a.steps == 2
    assert pair.b.steps == 2
    assert pair.distance == 10


def test_random_meets_distance() -> None:
    """
    ============================================================================
     Factory.random enforces min_distance.
    ============================================================================
    """
    grid = GridMap(rows=20, cols=20)
    pair = PairCluster.Factory.random(
        grid=grid, min_cells_a=5, min_cells_b=5,
        steps=2, min_distance=10)
    assert pair.distance >= 10


def test_random_disjoint() -> None:
    """
    ============================================================================
     Factory.random ensures cluster cells are disjoint.
    ============================================================================
    """
    grid = GridMap(rows=20, cols=20)
    pair = PairCluster.Factory.random(
        grid=grid, min_cells_a=5, min_cells_b=5,
        steps=2, min_distance=10)
    a_keys = {c.key for c in pair.a}
    b_keys = {c.key for c in pair.b}
    assert len(a_keys & b_keys) == 0


def test_random_asymmetric_cells() -> None:
    """
    ============================================================================
     Factory.random respects asymmetric min_cells_a vs min_cells_b.
    ============================================================================
    """
    grid = GridMap(rows=20, cols=20)
    pair = PairCluster.Factory.random(
        grid=grid, min_cells_a=3, min_cells_b=10,
        steps=2, min_distance=8)
    assert len(pair.a) >= 3
    assert len(pair.b) >= 10


def test_random_raises_when_impossible() -> None:
    """
    ============================================================================
     Factory.random raises ValueError when constraints are unmeetable.
    ============================================================================
    """
    grid = GridMap(rows=5, cols=5)
    with pytest.raises(ValueError):
        PairCluster.Factory.random(
            grid=grid,
            min_cells_a=3,
            min_cells_b=3,
            steps=1,
            min_distance=1000,
            max_tries=10)


def test_str_and_repr() -> None:
    """
    ============================================================================
     __str__ and __repr__ contain the distance.
    ============================================================================
    """
    pair = PairCluster.Factory.a()
    s = str(pair)
    r = repr(pair)
    assert 'distance=10' in s
    assert 'distance=10' in r
