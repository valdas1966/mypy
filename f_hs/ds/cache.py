from __future__ import annotations  
from f_core.mixins.dictable.main import Dictable
from f_hs.ds.path import Path, Node


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
        
    def __str__(self) -> str:
        """
        =======================================================================
         Return the string representation of the cache.
        =======================================================================
        """
        s = 'Cache:\n'
        for node in reversed(sorted(self._data.keys())):
            path = self._data[node]
            s += f'{node.cell.to_tuple()}: {[n.cell.to_tuple() for n in path]}\n'
        return s
    
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
        for i, node in enumerate(path):
            cache[node] = path[i:]
        return cache
