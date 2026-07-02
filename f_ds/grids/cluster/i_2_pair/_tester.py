import random

from f_ds.grids import GridMap as Grid
from f_ds.grids.cluster.i_2_pair import PairCluster


def test_distance() -> None:
    """
    ========================================================================
     Test distance() — Manhattan between centers (2,2) and (7,7) = 10.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    expected = pair.cluster_a.center.distance(other=pair.cluster_b.center)
    assert pair.distance() == expected
    assert pair.distance() == 10


def test_iter() -> None:
    """
    ========================================================================
     Test __iter__() — unpacking `a, b = pair`.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair
    assert a is pair.cluster_a
    assert b is pair.cluster_b


def test_getitem() -> None:
    """
    ========================================================================
     Test __getitem__() — pair[0] / pair[1].
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    assert pair[0] is pair.cluster_a
    assert pair[1] is pair.cluster_b


def test_random_many_cross_product() -> None:
    """
    ========================================================================
     random_many returns the full A x B cross product of two distinct
     pools -- up to many*many PairClusters, all distinct.
    ========================================================================
    """
    random.seed(0)
    grid = Grid(rows=10)
    pairs = PairCluster.Factory.random_many(grid=grid, many=4, steps_a=0,
                                            steps_b=1)
    assert 0 < len(pairs) <= 16
    assert len(set(pairs)) == len(pairs)
    assert all(isinstance(p, PairCluster) for p in pairs)


def test_random_many_min_dist() -> None:
    """
    ========================================================================
     min_dist filters the cross product to pairs whose center-to-center
     distance() is at least min_dist.
    ========================================================================
    """
    random.seed(0)
    grid = Grid(rows=10)
    pairs = PairCluster.Factory.random_many(grid=grid, many=6, steps_a=0,
                                            steps_b=0, min_dist=5)
    assert all(p.distance() >= 5 for p in pairs)


def test_random_many_best_effort() -> None:
    """
    ========================================================================
     On a grid too small to supply `many` distinct diamonds, random_many
     degrades gracefully (fewer pairs, no raise).
    ========================================================================
    """
    random.seed(0)
    grid = Grid(rows=2)        # 4 valid cells -> at most 4 distinct centers
    pairs = PairCluster.Factory.random_many(grid=grid, many=99, steps_a=0,
                                            steps_b=0)
    assert 0 < len(pairs) <= 16    # <= 4 A x 4 B
