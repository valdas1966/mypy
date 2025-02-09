from f_core.abstracts.dictable import Dictable
from f_graph.path.node import NodePath as Node
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
    path: Callable[[], list[Node]]
    distance: Callable[[], int]


class Cache(Dictable[Node, DataCache]):
    """
    ===========================================================================
     Cache for storing the data for each cached node.
    ===========================================================================
    """
    pass

    @classmethod
    def from_explored(cls, explored: set[Node]) -> 'Cache':
        """
        =======================================================================
         Create Cache from Explored-Set of Nodes.
        =======================================================================
        """
        cache = Cache()
        for node in explored:
            path = lambda n=node: list(reversed(n.path_from_root()[:-1]))
            distance = lambda n=node: n.g
            data = DataCache(path=path, distance=distance)
            cache[node] = data
        return cache

    @classmethod
    def from_path(cls, path: list[Node]) -> 'Cache':
        """
        =======================================================================
         Create Cache from Path.
        =======================================================================
        """
        cache = Cache()
        goal = path[-1]
        for node in path:
            path_from_node = lambda n=node, g=goal: g.path_from_node(node=n)[1:]
            distance = lambda n=node: len(path_from_node(n))
            data = DataCache(path=path_from_node, distance=distance)
            cache[node] = data
        return cache
