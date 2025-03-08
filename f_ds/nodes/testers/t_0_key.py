from f_ds.nodes.generators.g_0_key import GenNodeKey


def test_init() -> None:
    """
    ========================================================================
     Test the init of NodeKey.
    ========================================================================
    """
    node = GenNodeKey.one()
    assert node.key == 1
    assert node.name == 'One'


def test_clone() -> None:
    """
    ========================================================================
     Test the clone of NodeKey.
    ========================================================================
    """
    node = GenNodeKey.one()
    cloned = node.clone()
    assert cloned.key == node.key
    assert cloned.name == node.name
    cloned._key = 2
    assert cloned.key != node.key


def test_str() -> None:
    """
    ========================================================================
     Test the str of NodeKey.
    ========================================================================
    """
    node = GenNodeKey.one()
    assert str(node) == 'One(1)'


def test_hash() -> None:
    """
    ========================================================================
     Test the hash of NodeKey.
    ========================================================================
    """
    node_1 = GenNodeKey.one()
    node_2 = GenNodeKey.one()
    assert hash(node_1) == hash(node_2)
    node_2._name = 'Two'
    assert hash(node_1) == hash(node_2)
