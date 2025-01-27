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
