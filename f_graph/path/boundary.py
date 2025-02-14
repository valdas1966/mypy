from __future__ import annotations
from f_core.abstracts.dictable import Dictable
from f_cs.mixins.has_eager import HasEager
from f_graph.path.path import Path, Node
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.cache import Cache
from typing import Callable


class Boundary(Dictable[Node, Callable[[], int]], HasEager):
    """
    ========================================================================
    """
    def __init__(self,
                 graph: Graph,
                 cache: Cache,
                 path: Path,
                 is_eager: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Dictable.__init__(self)
        HasEager.__init__(self, is_eager=is_eager)
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
            children = self._graph.children(node=node)
            for child in children:
                if child in self._cache:
                    continue
                self._data[child] = lambda: self._boundary_min(node=child)
                if self._is_eager:
                    self._data[child] = self._boundary_min(node=child)

    def _boundary_min(self, node: Node) -> int:
        """
        ====================================================================
         Get the Minimum Boundary for heuristic distance from Node to Goal.
        ====================================================================
        """
        distance_from_goal = self._path.goal.g - node.g
        return distance_from_goal - 1
    