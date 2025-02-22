from __future__ import annotations  
from f_core.abstracts.dictable import Dictable
from f_graph.path.path import Path, Node


class Cache(Dictable[Node, Path]):
    """
    ===========================================================================
     Cache for storing the data for each cached node.
    ===========================================================================
    """

    def update(self, cache: Cache) -> None:
        """
        =======================================================================
         Update the cache with the given cache.
        =======================================================================
        """
        Dictable.update(self, data=cache)
        
    @classmethod
    def from_explored(cls, explored: set[Node]) -> Cache:
        """
        =======================================================================
         Create Cache from Explored-Set of Nodes.
        =======================================================================
        """
        cache = Cache()
        for node in explored:
            cache[node] = reversed(node.path_from_root())
        return cache

    @classmethod
    def from_path(cls, path: Path) -> Cache:
        """
        =======================================================================
         Create Cache from Path.
        =======================================================================
        """    
        cache = Cache()
        for node in path:
            cache[node] = path.goal.path_from_node(node=node)
        return cache
