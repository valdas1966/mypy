from f_graph.data.i_0_abc import DataABC, NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


class DataOneToOne(DataABC[Node]):
    """
    ============================================================================
     Class of Data for One-to-One Path-Algorithm.
    ============================================================================
    """
    pass
