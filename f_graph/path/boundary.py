from __future__ import annotations
from collections import defaultdict
from f_core.abstracts.dictable import Dictable  
from f_graph.path.path import Path, Node
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.heuristic import Heuristic
from f_graph.path.cache import Cache


class Boundary(Dictable[Node, int]):
    """
    ========================================================================
     Bottom-Boundary Heuristic for Nodes in Path-Finding Algorithms.
    ========================================================================
    """

    def __init__(self) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Dictable.__init__(self)
        self._changed: set[Node] = set()
        self._stats_changed: dict[int, int] = defaultdict(int)

    @property
    def stats_changed(self) -> dict[int, int]:
        """
        ====================================================================
         Get the stats of the changed nodes.
        ====================================================================
        """
        return self._stats_changed

    def changed(self) -> set[Node]:
        """
        ====================================================================
         Get the changed nodes.
        ====================================================================
        """
        return self._changed
    
    def add_changed(self, node: Node, depth: int) -> None:
        """
        ====================================================================
         Add a changed node to the boundary.
        ====================================================================
        """
        self._changed.add(node)
        self._stats_changed[depth] += 1

    def remove_changed(self, node: Node) -> None:
        """
        ====================================================================
         Remove a changed node from the boundary.
        ====================================================================
        """
        self._changed.remove(node)

    def __str__(self) -> str:
        """
        ====================================================================
         String representation of the Boundary.
        ====================================================================
        """
        d = {node.cell.to_tuple(): self[node] for node in self}
        return str(d)

    @classmethod    
    def from_path(cls,
                  path: Path,
                  graph: Graph,
                  heuristic: Heuristic,
                  cache: Cache = None,
                  depth: int = 1) -> Boundary:
        """
        ====================================================================
         Build the Boundary from the Path.
        ====================================================================
        """        
        # If the cache is not provided, create a new one
        cache = cache if cache else Cache()
        # Initialize the boundary
        boundary = cls()
        # Iterate over the path nodes
        for node in path:
            # Get the children of the node
            children = graph.children(node=node)
            # Iterate over the children
            for child in children:
                # If the child is in the cache, skip it
                if child in cache:
                    continue
                # Get the lower bound of the child
                bound = path.goal.g - node.g - 1
                # If the child is not in the boundary, or the bound is lower than the
                #  current bound, update the bound and add the child to the changed set
                if child not in boundary or bound < boundary[child]:
                    boundary[child] = bound
                    # If the bound is more reliable than the heuristic,
                    #  add the child to the changed set
                    if bound > heuristic(child):
                        boundary.add_changed(node=child, depth=1)
            for d in range(2, depth+1):
                for node in list(boundary.changed()):
                    children = graph.children(node=node)
                    for child in children:
                        if child in cache:
                            continue
                        bound = boundary[node] - 1
                        if child not in boundary or bound < boundary[child]:
                            boundary[child] = bound
                            if bound > heuristic(child):
                                boundary.add_changed(node=child, depth=d)
                    boundary.remove_changed(node=node)
        return boundary
        