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
        self.update(explored=explored)

    def update(self, explored: set[Node]) -> None:
        """
        ========================================================================
         Update the Cache.
        ========================================================================
        """
        for node in explored:
            if node in self._data:
                continue
            path = lambda n=node: list(reversed(n.path_from()))
            distance = lambda n=node: n.g
            self._data[node] = DataCache(path=path, distance=distance)

