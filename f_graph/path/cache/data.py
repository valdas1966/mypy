from f_ds.nodes.i_1_heuristic import NodeHeuristic as Node
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
