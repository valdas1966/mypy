from f_ds.groups.generators.g_group import GenGroup


def test_group_distribute() -> None:
    """
    ========================================================================
     Test the distribute().
    ========================================================================
    """
    group = GenGroup.five()
    groups = group.distribute(n=2)
    assert len(groups) == 2
    assert groups[0].data == [1, 2, 3]
    assert groups[1].data == [4, 5]
