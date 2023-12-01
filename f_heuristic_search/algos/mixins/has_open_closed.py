from f_data_structure.priority_queue import PriorityQueue
from f_data_structure.nodes.i_0_base import NodeBase as Node


class HasOpenClosed:
    """
    ============================================================================
     Mixin for algorithms that utilize Open and Closed lists.
    ============================================================================
    """

    open: PriorityQueue  # Queue for Generated Nodes (not expanded yet).
    closed: set[Node]    # List of Expanded Nodes in insertion order.

    def __init__(self) -> None:
        self._open = PriorityQueue()
        self._closed = set()

    @property
    def open(self) -> PriorityQueue:
        return self._open

    @property
    def closed(self) -> set[Node]:
        return self._closed

    def _is_expanded(self, node: Node) -> bool:
        """
        ========================================================================
         Returns True if the given Node is have already been expanded.
        ========================================================================
        """
        return node in self.closed

    def _is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Returns True if the given Node is have already generated.
        ========================================================================
        """
        return node in self.open
