from __future__ import annotations
from f_core.abstracts.dictable import Dictable  
from f_graph.path.path import Path, Node
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.cache import Cache


class Boundary(Dictable[Node, int]):
    """
    ========================================================================
     Bottom-Boundary Heuristic for Nodes in Path-Finding Algorithms.
    ========================================================================
    """

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
                  cache: Cache = None) -> Boundary:
        """
        ====================================================================
         Build the Boundary from the Path.
        ====================================================================
        """        
        cache = cache if cache else Cache()
        boundary = cls()
        for node in path:
            children = graph.children(node=node)
            for child in children:
                if child in cache:
                    continue
                bound = path.goal.g - node.g - 1
                if child in boundary:
                    boundary[child] = min(boundary[child], bound)
                else:
                    boundary[child] = bound
        return boundary
        