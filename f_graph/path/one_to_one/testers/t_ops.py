from f_graph.path.one_to_one.generators.g_ops import GenOps
from f_graph.path.one_to_one.ops import OpsOneToOne, TypeCounter
import pytest


@pytest.fixture         
def ops() -> OpsOneToOne:
    return GenOps.gen_3x3()


def test_generate(ops: OpsOneToOne) -> None:
    """
    ========================================================================
     Test generate method.
    ========================================================================
    """
    # Non-Cached Node
    node = ops._problem.graph[0, 0]
    ops.generate(node=node, parent=None)
    assert node in ops._state.generated
    assert node.parent is None
    assert node.h == 0
    assert not node.is_cached
    
    # Cached Node
    cached = ops._problem.graph[0, 1]
    ops.generate(node=cached, parent=node)
    assert cached in ops._state.generated 
    assert cached.parent == node
    assert cached.h == 3
    assert cached.is_cached

    # Check Counter
    assert ops._counter[TypeCounter.GENERATED] == 2
    assert ops._counter[TypeCounter.EXPLORED] == 0


def test_explore(ops: OpsOneToOne) -> None:
    """
    ========================================================================
     Test explore method.
    ========================================================================
    """
    # Explore
    node = ops._problem.graph[2, 2]
    child_1 = ops._problem.graph[1, 2]
    child_2 = ops._problem.graph[2, 1]
    child_1.parent = node
    child_2.parent = node
    ops.explore(node=node)
    assert node in ops._state.explored
    assert child_1 in ops._state.generated
    assert child_2 in ops._state.generated

    # Check Counter
    assert ops._counter[TypeCounter.EXPLORED] == 1
    assert ops._counter[TypeCounter.GENERATED] == 2
