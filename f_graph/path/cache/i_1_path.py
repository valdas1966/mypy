from f_graph.path.cache.i_0_base import Cache, DataCache, Node

class CachePath(Cache):
    """
    ========================================================================
     Cache from Path.
    ========================================================================
    """

    def __init__(self, path: list[Node]) -> None:
        """
        ========================================================================
         Initialize the Cache.
        ========================================================================
        """
        Cache.__init__(self)
        for node in reversed(path):
            
