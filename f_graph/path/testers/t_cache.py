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
    

def test_str_explored() -> None:
    """
    ============================================================================
     Test str() method with Explored-Cache.
    ============================================================================
    """
    cache = GenCache.from_explored()
    node_1, node_2, node_3 = GenNode.first_row_branch_3x3()
    str_true = 'Cache:\n'
    str_true += f'{node_1.uid.to_tuple()}: [(0, 0)]\n'
    str_true += f'{node_2.uid.to_tuple()}: [(0, 1), (0, 0)]\n'
    str_true += f'{node_3.uid.to_tuple()}: [(0, 2), (0, 1), (0, 0)]\n'
    assert str(cache) == str_true


def test_str_path() -> None:
    """
    ============================================================================
     Test str() method with Path-Cache.
    ============================================================================
    """
    cache = GenCache.from_path()
    node_1, node_2, node_3 = GenNode.first_row_branch_3x3()
    str_true = 'Cache:\n'
    str_true += f'{node_1.uid.to_tuple()}: {[(0, 0), (0, 1), (0, 2)]}\n'
    str_true += f'{node_2.uid.to_tuple()}: {[(0, 1), (0, 2)]}\n'
    str_true += f'{node_3.uid.to_tuple()}: {[(0, 2)]}\n'
    assert str(cache) == str_true
