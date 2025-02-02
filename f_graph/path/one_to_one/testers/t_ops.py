from f_graph.path.one_to_one.generators.g_ops import GenOps


def test_generate() -> None:
    """
    ========================================================================
     Test generate method.
    ========================================================================
    """
    # Setup
    ops = GenOps.gen_3x3()

    # Non-Cached Node
    node = ops._problem.graph[0, 0]
    ops.generate(node=node, parent=None)
    assert node in ops._state.generated
    assert node.parent is None
    assert node.h is None
    assert not node.is_cached
    
    # Cached Node
    cached = ops._problem.graph[1, 2]
    ops.generate(node=cached, parent=node)
    assert cached in ops._state.generated 
    assert cached.parent == node
    assert cached.h == 1
    assert cached.is_cached


def test_explore() -> None:
    """
    ========================================================================
     Test explore method.
    ========================================================================
    """
    # Setup
    ops = GenOps.gen_3x3()

    # Explore
    node = ops._problem.graph[0, 0]
    child = ops._problem.graph[0, 1]
    ops.explore(node=node)
    assert node in ops._state.explored
    assert child in ops._state.generated
