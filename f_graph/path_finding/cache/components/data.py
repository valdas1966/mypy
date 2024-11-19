from f_graph.path_finding.config import Problem, Queue, Node, Data as DataPath
from typing import Type


class Data(DataPath[Node]):
    """
    ============================================================================
     Data objects for Path-Algorithms with Cache.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[Node],
                 type_queue: Type[Queue]):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataPath.__init__(self, problem=problem, type_queue=type_queue)
        self._cache = cache

    def is_cached(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node is Cached.
        ========================================================================
        """
        return node in self._cache
