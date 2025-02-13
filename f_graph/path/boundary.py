from __future__ import annotations
from f_core.abstracts.dictable import Dictable
from f_graph.path.path import Path, Node
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.cache import Cache
from typing import Generic, TypeVar

T = TypeVar('T')


class BoundaryGeneric(Generic[T], Dictable[Node, T]):
    """
    ========================================================================
    """
    def __init__(self,
                 graph: Graph,
                 cache: Cache,
                 path: Path) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Dictable.__init__(self)
        self._graph = graph
        self._cache = cache
        self._path = path
        self._build_from_path()

    def _build_from_path(self) -> None:
        """
        ====================================================================
         Build the Boundary from the Path.
        ====================================================================
        """
        for node in self._path:
            distance = self._distance_from_goal(node=node)
            if distance == 0:
                continue
            children = self._graph.children(node=node)
            for child in children:
                if child in self._cache:
                    continue
                self._data[child] = distance - 1

    def _distance_from_goal(self, node: Node) -> int:
        """
        ====================================================================
         Get the Distance from the Node to the Goal.
        ====================================================================
        """
        return self._path.goal.g - node.g
