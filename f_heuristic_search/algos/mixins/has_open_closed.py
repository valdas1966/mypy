from queue import PriorityQueue
from ordered_set import OrderedSet


class HasOpenClosed:
    """
    ============================================================================
     Mixin for algorithms that utilize Open and Closed lists.
    ============================================================================
    """

    open: PriorityQueue       # Queue for Generated Nodes (not expanded yet).
    closed: OrderedSet        # List of Expanded Nodes in insertion order.

    def __init__(self) -> None:
        self._open = PriorityQueue()
        self._closed = OrderedSet()

    @property
    def open(self) -> PriorityQueue:
        return self._open

    @property
    def closed(self) -> OrderedSet:
        return self._closed
