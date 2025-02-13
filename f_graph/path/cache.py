from __future__ import annotations  
from f_core.abstracts.dictable import Dictable
from f_graph.path.node import NodePath as Node
from f_graph.path.path import Path
from dataclasses import dataclass
from typing import Callable


@dataclass
class DataCache:
    """
    ===========================================================================
     Cache Data that stores for each node:
    ---------------------------------------------------------------------------
        1. Optimal-Path from Node to Goal.
        2. True-Distance from Node to Goal.
    ===========================================================================
    """
    path: Callable[[], Path]
    distance: Callable[[], int]

    def __eq__(self, other: DataCache) -> bool:
        """
        =======================================================================
         Check if the two DataCache objects are equal.
        =======================================================================
        """
        p_1 = self.path() == other.path()
        p_2 = self.distance() == other.distance()
        return p_1 and p_2


class Cache(Dictable[Node, DataCache]):
    """
    ===========================================================================
     Cache for storing the data for each cached node.
    ===========================================================================
    """
    pass

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
            path = lambda n=node: reversed(n.path_from_root())
            distance = lambda n=node: n.g
            data = DataCache(path=path, distance=distance)
            cache[node] = data
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
            path_from_node = lambda n=node, g=path.goal: g.path_from_node(node=n)
            distance = lambda n=node: len(path_from_node(n)) - 1
            data = DataCache(path=path_from_node, distance=distance)
            cache[node] = data
        return cache
