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
            path = lambda: node.path_from()
            distance = lambda: node.g
            self._data[node] = DataCache(path=path, distance=distance)

