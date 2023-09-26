from f_data_structure.priority_queue import PriorityQueue


class HasOpenClosed:
    """
    ============================================================================
     Mixin for algorithms that utilize Open and Closed lists.
    ============================================================================
    """

    open: PriorityQueue       # Queue for Generated Nodes (not expanded yet).
    closed: set               # Set of Expanded (visited) Nodes.

    def __init__(self) -> None:
        self._open = PriorityQueue()
        self._closed = set()

    @property
    def open(self) -> PriorityQueue:
        return self._open

    @property
    def closed(self) -> set:
        return self._closed
