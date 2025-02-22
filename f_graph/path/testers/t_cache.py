from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_node import GenNode


def test_from_explored():
    """
    ============================================================================
     Test from_explored() method.
    ============================================================================
    """
    cache = GenCache.from_explored()
    node_1, node_2, node_3 = GenNode.first_row_branch_3x3()
    assert cache[node_1] == [node_1]
    assert cache[node_2] == [node_2, node_1]
    assert cache[node_3] == [node_3, node_2, node_1]


def test_from_path():
    """
    ============================================================================
     Test from_path() method.
    ============================================================================
    """
    cache = GenCache.from_path()
    node_1, node_2, node_3 = GenNode.first_row_branch_3x3()
    assert cache[node_1] == [node_1, node_2, node_3]
    assert cache[node_2] == [node_2, node_3]
    assert cache[node_3] == [node_3]
    