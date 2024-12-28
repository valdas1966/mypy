from f_graph.path.cache.data import DataCache, Node
from f_core.abstracts.dictable import Dictable


class Cache(Dictable[Node, DataCache]):
    """
    ========================================================================
     Base Class for Cache.
    ========================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Dictable.__init__(self)
