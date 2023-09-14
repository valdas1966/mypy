from f_data_structure.priority_queue import PriorityQueue


class OpenClosed:
    """
    ============================================================================
     Mixin Class for Algorithms that use Open and Closed lists.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. open (PriorityQueue)          : Generated Nodes (not expanded yet).
        2. closed (set)                  : Expanded Nodes.
    ============================================================================
    """

    def __init__(self) -> None:
        self._open = PriorityQueue()
        self._closed = set()

    @property
    def open(self) -> PriorityQueue:
        return self._open

    @property
    def closed(self) -> set:
        return self._closed
