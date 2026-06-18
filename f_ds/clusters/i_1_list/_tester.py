from f_ds.clusters.i_1_list.main import ClusterList


def test_collectionable() -> None:
    """
    ========================================================================
     len / in / iter / bool come from Collectionable via to_iterable().
    ========================================================================
    """
    cluster = ClusterList(members=[1, 2, 3])

    actual = (len(cluster), 2 in cluster, 9 in cluster,
              sorted(cluster), bool(cluster))

    expected = (3, True, False, [1, 2, 3], True)

    assert actual == expected


def test_bool_empty() -> None:
    """
    ========================================================================
     An empty ClusterList is falsy.
    ========================================================================
    """
    cluster = ClusterList(members=[])

    actual = bool(cluster)

    expected = False

    assert actual == expected


def test_name() -> None:
    """
    ========================================================================
     Identity (name) is exposed via HasName; defaults to 'ClusterList'.
    ========================================================================
    """
    cluster = ClusterList(members=[1], name='K')

    actual = (cluster.name, ClusterList(members=[1]).name)

    expected = ('K', 'ClusterList')

    assert actual == expected


def test_members_is_copy() -> None:
    """
    ========================================================================
     members returns a list copy; mutating it does not touch the Cluster.
    ========================================================================
    """
    cluster = ClusterList(members=[1, 2, 3])
    members = cluster.members
    members.append(99)

    actual = (members, len(cluster))

    expected = ([1, 2, 3, 99], 3)

    assert actual == expected


def test_representative() -> None:
    """
    ========================================================================
     representative is the passed-in value; default None.
    ========================================================================
    """
    cluster = ClusterList(members=[5, 2, 8], representative=2)

    actual = (cluster.representative, ClusterList(members=[1]).representative)

    expected = (2, None)

    assert actual == expected


def test_str_repr() -> None:
    """
    ========================================================================
     __str__ shows name + size + representative (when present); __repr__
     comes from HasRepr and wraps __str__ as '<Cls: str>'.
    ========================================================================
    """
    cluster = ClusterList(members=[1, 2, 3], name='K', representative=1)

    actual = (str(cluster), repr(cluster))

    expected = ('K(size=3, rep=1)', '<ClusterList: K(size=3, rep=1)>')

    assert actual == expected


def test_str_no_representative() -> None:
    """
    ========================================================================
     With no representative, 'rep=' is omitted from the string forms.
    ========================================================================
    """
    cluster = ClusterList(members=[4, 5], name='E')

    actual = (str(cluster), repr(cluster))

    expected = ('E(size=2)', '<ClusterList: E(size=2)>')

    assert actual == expected
