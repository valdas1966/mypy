from f_core.abstracts.dictable import Dictable
from f_graph.path.graph import GraphPath as Graph
from f_graph.path.cache import Cache


class Boundary(Dictable):
    """
    ========================================================================
    """
    def __init__(self,
                 graph: Graph,
                 cache: Cache,
                 path
                 boundary: 'Boundary') -> None:
