from f_graph.path.components.solution import Path
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphGrid)
Node = TypeVar('Node', bound=NodeCell)


class Path(Generic[Node], PathBase[Node]):

    def __init__(self,
                 graph: Graph,
                 cache: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        PathBase.__init__(self, graph=graph)
        self._cache = {node: node for node in cache}

    def construct(self, goal: Node) -> None:
        """
        ========================================================================
         Construct an Optimal-Path from Start to Goal.
        ========================================================================
        """
        PathBase.construct(self, goal=goal)
        if goal in self._cache:
            path_cached = self._cache[goal].path_from_start()[1:]
            path_cached_reversed = reversed(path_cached)
            self._paths[goal] += path_cached_reversed
