from f_hs.problems.base import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)

class HasStart(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Finding-Problems with a single Start-Node.
     ===========================================================================
    """

    def __init__(self, start: Node) -> Node:
        self._start = start

    @property
    def start(self) -> Node:
        return self._start
