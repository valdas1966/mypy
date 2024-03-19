from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class HasStart(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Problems with a Start Node.
    ============================================================================
    """

    def __init__(self, start: Node) -> None:
        self._start = start

    @property
    def start(self) -> Node:
        return self._start
