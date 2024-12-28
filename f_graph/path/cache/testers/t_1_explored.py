from f_graph.path.cache.i_1_explored import CacheExplored, Node


def test_cache_explored() -> None:
    """
    ========================================================================
     Test Cache Explored.
    ========================================================================
    """
    node = Node.generate_zero()
    explored: set[Node] = {node}
    cache = CacheExplored(explored)
    assert cache[node].path() == [node]
    assert cache[node].distance() == 0
