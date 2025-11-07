from f_graph.nodes.i_1_parent import NodeParent
import pytest


@pytest.fixture
def nodes_abc() -> list[NodeParent[str]]:
    """
    ========================================================================
     Fixture for the nodes.
    ========================================================================
    """
    node_a = NodeParent.Factory.a()
    node_b = NodeParent.Factory.b()
    node_c = NodeParent.Factory.c()
    return [node_a, node_b, node_c]


def test_path_from_root(nodes_abc: list[NodeParent[str]]) -> None:
    """
    ========================================================================
     Test the path_from_root() method of NodeParent.
    ========================================================================
    """
    node_a, node_b, node_c = nodes_abc
    assert node_a.path_from_root() == [node_a]
    assert node_b.path_from_root() == [node_a, node_b]
    assert node_c.path_from_root() == [node_a, node_b, node_c]


def test_path_from_node(nodes_abc: list[NodeParent[str]]) -> None:
    """
    ========================================================================
     Test the path_from_node() method of NodeParent.
    ========================================================================
    """
    node_a, node_b, node_c = nodes_abc
    assert node_c.path_from_node(node_a) == [node_a, node_b, node_c]
    assert node_c.path_from_node(node_b) == [node_b, node_c]
    assert node_a.path_from_node(node_a) == [node_a]
    assert node_a.path_from_node(node_b) == []
