from __future__ import annotations
from f_core.abstracts.dictable import Dictable  
from f_cs.mixins.has_eager import HasEager
from f_graph.path.path import Path, Node
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.cache import Cache
from typing import Callable


class Boundary(Dictable[Node, Callable[[], int]]):
    """
    ========================================================================
    """
    def __init__(self) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        Dictable.__init__(self)

    def __getitem__(self, node: Node) -> Callable[[], int]:
        """
        ====================================================================
         Get the Boundary for a Node.
        ====================================================================
        """
        return self._data.get(node, lambda: 0)
        
    @staticmethod    
    def bottom(node: Node, goal: Node) -> int:
        """
        ====================================================================
         Get the Minimum Boundary for heuristic distance from Node to Goal.
        ====================================================================
        """ 
        distance_from_goal = goal.g - node.g
        return distance_from_goal - 1

    @classmethod    
    def from_path(cls,
                  path: Path,
                  graph: Graph,
                  cache: Cache = None,
                  is_eager: bool = False,
                 ) -> Boundary:
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
                bottom = lambda n=node, g=path.goal: Boundary.bottom(n, g)
                boundary[child] = bottom
                if is_eager:
                    Boundary.bottom(node=node, goal=path.goal)       
        return boundary
        
    