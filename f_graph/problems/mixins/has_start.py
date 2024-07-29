from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasStart(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Graph-Problems with single Start-Node.
    ============================================================================
    """

    def __init__(self, start: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._start = start

    @property
    def start(self) -> Node:
        return self._start
