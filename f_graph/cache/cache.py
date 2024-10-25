from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar, Generic, Callable

Node = TypeVar('Node', bound=NodePath)


class Cache(Generic[Node]):
    """
    ============================================================================
     Cache for Path-Algorithms.
    ============================================================================
    """

    def __init__(self, cache: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ------------------------------------------------------------------------
         Cache is stored as a Dict for retrieval.
        ========================================================================
        """
        self._cache: dict[Node, Node] = {node: node for node in cache}

    def __contains__(self, item: Node) -> bool:
        """
        ========================================================================
         Return True if the received Node is in the Cache.
        ========================================================================
        """
        return item in self._cache

    def path_to_goal(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return the Optimal-Path from the received cached Node to Goal.
        ========================================================================
        """
        path = self._cache[node].path_from_start()
        path.reverse()
        return path

    def accurate_distance_to_goal(self, node: Node) -> int:
        """
        ========================================================================
         Return an accurate distance to Goal from the received cached Node.
        ========================================================================
        """
        return self._cache[node].g
