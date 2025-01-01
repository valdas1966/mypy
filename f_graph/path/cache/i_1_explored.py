from f_graph.path.cache.i_0_base import Cache, DataCache, Node


class CacheExplored(Cache):
    """
    ========================================================================
     Cache from Explored-Nodes.
    ========================================================================
    """

    def __init__(self, explored: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Cache.__init__(self)
        for node in explored:
            path = lambda n=node: list(reversed(n.path_from()))
            distance = lambda n=node: n.g
            self._data[node] = DataCache(path=path, distance=distance)

