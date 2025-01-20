from f_core.abstracts.dictable import Dictable
from f_graph.path.node import NodePath as Node



class Cache(Dictable[Node, DataCache]):
    """
    ========================================================================
     Cache for One-to-One Path-Algorithms.
    ========================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
