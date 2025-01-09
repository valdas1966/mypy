from f_graph.path.node import NodePath as Node
from dataclasses import dataclass
from typing import Callable


@dataclass
class DataCache:
    """
    ========================================================================
     Data-Cache Class.
    ========================================================================
    """
    path: Callable[[], list[Node]]
    distance: Callable[[], int]
