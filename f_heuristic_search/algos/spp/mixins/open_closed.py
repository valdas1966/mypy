from f_data_structure.priority_queue import PriorityQueue


class OpenClosed:
    """
    ============================================================================
     Desc: Mixin Class for Algorithms that use Open and Closed lists.
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
