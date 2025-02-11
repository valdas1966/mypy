from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_graph import GenGraphPath


def test_gen_3x3():
    """
    ============================================================================
     Test gen_3x3() method.
    ============================================================================
    """
    cache = GenCache.gen_3x3()
    graph = GenGraphPath.gen_3x3()
    node = graph[0, 1]
    assert cache[node].path() == [graph[0, 2], graph[1, 2], graph[2, 2]]
    assert cache[node].distance() == 3


def test_gen_3x3_from_explored():
    """
    ============================================================================
     Test gen_3x3_from_explored() method.
    ============================================================================
    """
    cache = GenCache.gen_3x3_from_explored()
    graph = GenGraphPath.gen_3x3()
    node_1 = graph[1, 2]
    node_2 = graph[2, 2]
    assert cache[node_1].path() == [node_2]
    assert cache[node_1].distance() == 1
    assert cache[node_2].path() == []
    assert cache[node_2].distance() == 0


def test_gen_3x3_from_path():
    """
    ============================================================================
     Test gen_3x3_from_path() method.
    ============================================================================
    """
    cache = GenCache.gen_3x3_from_path()
    graph = GenGraphPath.gen_3x3()
    node_1 = graph[0, 1]
    node_2 = graph[0, 2]
    node_3 = graph[1, 2]
    node_4 = graph[2, 2]
    assert cache[node_1].path() == [node_2, node_3, node_4]
    assert cache[node_1].distance() == 3
    assert cache[node_2].path() == [node_3, node_4]
    assert cache[node_2].distance() == 2
    assert cache[node_3].path() == [node_4]
    assert cache[node_3].distance() == 1
    assert cache[node_4].path() == []
    assert cache[node_4].distance() == 0
    

def test_data_cache():
    """
    ============================================================================
     Test data_cache() method.
    ============================================================================
    """
    cache_1 = GenCache.gen_data_cache()   
    cache_2 = GenCache.gen_data_cache()
    assert cache_1 == cache_2


def test_update():
    """
    ============================================================================
     Test update() method.
    ============================================================================
    """
    cache_explored = GenCache.gen_3x3_from_explored()
    cache_path = GenCache.gen_3x3_from_path()
    cache_explored.update(cache_path)
    uids_explored = {node.uid for node in cache_explored.keys()}
    uids_path = {node.uid for node in cache_path.keys()}
    assert uids_explored == uids_path
    
