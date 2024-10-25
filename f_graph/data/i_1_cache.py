from f_graph.data.i_0_abc import DataABC, Node, QueueBase
from typing import Type


class DataCache(DataABC[Node]):
    """
    ============================================================================
     Data-Object with Cache for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 type_queue: Type[QueueBase],
                 cache: set[Node] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataABC.__init__(self, type_queue=type_queue)
        self._cache = cache or set()

    def is_cached(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the received Node is cached.
        ========================================================================
        """
        return node in self._cache

    def cache_path(self, node: Node) -> list[Node]:
        path = node.path_from_root()[:-1]
        return reversed(path)
    