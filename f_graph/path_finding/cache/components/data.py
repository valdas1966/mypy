from f_graph.path_finding.config import Problem, Queue, TNode, Data as DataPath
from typing import Type


class Data(DataPath[TNode]):
    """
    ============================================================================
     Data objects for Path-Algorithms with Cache.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[TNode],
                 type_queue: Type[Queue]):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataPath.__init__(self, problem=problem, type_queue=type_queue)
        self._cache = cache

    def is_cached(self, node: TNode) -> bool:
        """
        ========================================================================
         Return True if the Node is Cached.
        ========================================================================
        """
        return node in self._cache
