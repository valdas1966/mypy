from f_data_structure.open import Open
from f_data_structure.closed import Closed


class HasOpenClosed:
    """
    ============================================================================
     Mixin for algorithms that utilize Open and Closed lists.
    ============================================================================
    """

    open: Open            # Queue for Generated Nodes (not expanded yet).
    closed: Closed        # List of Expanded Nodes in insertion order.

    def __init__(self) -> None:
        self._open = Open()
        self._closed = Closed()

    @property
    def open(self) -> Open:
        return self._open

    @property
    def closed(self) -> Closed:
        return self._closed
