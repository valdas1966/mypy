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
