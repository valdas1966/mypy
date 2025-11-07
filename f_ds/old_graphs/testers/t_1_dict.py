from f_ds.old_graphs.generators.g_1_dict import GenGraphDict
from f_graph.nodes import NodeKey


def test_nodes() -> None:
    """
    ========================================================================
     Test the old_nodes() method.
    ========================================================================
    """
    graph = GenGraphDict.two()
    nodes_true = [NodeKey(key=1), NodeKey(key=2)]
    assert graph.nodes() == nodes_true


def test_nodes_by_keys() -> None:
    """
    ========================================================================
     Test the nodes_by_keys() method.
    ========================================================================
    """
    graph = GenGraphDict.two()
    node_1 = graph.nodes_by_keys(key=1)
    node_2 = graph.nodes_by_keys(key=2)
    nodes_true = [NodeKey(key=1), NodeKey(key=2)]
    assert [node_1, node_2] == nodes_true


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """
    graph_1 = GenGraphDict.two()
    graph_2 = GenGraphDict.two()
    graph_3 = GenGraphDict.one()
    assert graph_1 == graph_2
    assert graph_1 != graph_3
