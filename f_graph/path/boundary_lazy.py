from f_core.abstracts.dictable import Dictable
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.node import NodePath as Node
from f_graph.path.cache import Cache
from f_graph.path.path import Path
from typing import Callable


class BoundaryLazy(Dictable[Node, Callable[[], int]]):
    """
    ========================================================================
    
    ========================================================================
    """

    def __init__(self, graph: Graph, cache: Cache, path: Path) -> None:
        """
        ====================================================================
        
        ====================================================================
        """
        Dictable.__init__(self)
        self._graph = graph
        self._cache = cache
        self._path = path

    def __getitem__(self, key: Node) -> int:
        """
        """
