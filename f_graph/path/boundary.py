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
                # If the child is in the boundary, update the bound
                if child in boundary:
                    boundary[child] = min(boundary[child], bound)
                # Otherwise, add the child to the boundary
                else:
                    boundary[child] = bound
                """
                # Get the grandchildren of the child
                grandchildren = graph.children(node=child)
                # Iterate over the grandchildren
                for grandchild in grandchildren:
                    # If the grandchild is in the cache, skip it
                    if grandchild in cache:
                        continue
                    # Get the lower bound of the grandchild
                    grandbound = bound - 1
                    # If the grandchild is in the boundary, update the bound
                    if grandchild in boundary:
                        boundary[grandchild] = min(boundary[grandchild], grandbound)
                    # Otherwise, add the grandchild to the boundary
                    else:
                        boundary[grandchild] = grandbound
                """
        return boundary
        