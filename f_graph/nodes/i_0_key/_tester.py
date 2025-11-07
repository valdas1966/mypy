from f_graph.nodes.i_0_key import NodeKey


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison method of NodeKey.
    ========================================================================
    """
    node_a = NodeKey.Factory.a()
    node_b = NodeKey.Factory.b()
    assert node_a < node_b
    assert node_a != node_b
    assert node_a == node_a
    