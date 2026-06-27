from f_ds.grids.cluster.pair import PairCluster


def test_cluster_a_cluster_b() -> None:
    """
    ========================================================================
     Test the cluster_a and cluster_b accessors.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    assert pair.cluster_a is pair.key[0]
    assert pair.cluster_b is pair.key[1]


def test_eq() -> None:
    """
    ========================================================================
     Test the __eq__() method — same two clusters compare equal.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair.cluster_a, pair.cluster_b
    assert PairCluster(cluster_a=a, cluster_b=b) == \
        PairCluster(cluster_a=a, cluster_b=b)


def test_ordered() -> None:
    """
    ========================================================================
     Test ordering matters — (a, b) != (b, a).
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair.cluster_a, pair.cluster_b
    assert PairCluster(cluster_a=a, cluster_b=b) != \
        PairCluster(cluster_a=b, cluster_b=a)


def test_hash() -> None:
    """
    ========================================================================
     Test the __hash__() method — equal pairs dedup in a set.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair.cluster_a, pair.cluster_b
    p1 = PairCluster(cluster_a=a, cluster_b=b)
    p2 = PairCluster(cluster_a=a, cluster_b=b)
    assert hash(p1) == hash(p2)
    assert {p1, p2} == {p1}


def test_key() -> None:
    """
    ========================================================================
     Test the key property — (cluster_a, cluster_b).
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    assert pair.key == (pair.cluster_a, pair.cluster_b)


def test_str() -> None:
    """
    ========================================================================
     Test __str__() — 'PairCluster(str_a, str_b)'.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair.cluster_a, pair.cluster_b
    assert str(pair) == f'PairCluster({a}, {b})'


def test_repr() -> None:
    """
    ========================================================================
     Test __repr__() — '<PairCluster: repr_a | repr_b>'.
    ========================================================================
    """
    pair = PairCluster.Factory.diamonds()
    a, b = pair.cluster_a, pair.cluster_b
    assert repr(pair) == f'<PairCluster: {a!r} | {b!r}>'
