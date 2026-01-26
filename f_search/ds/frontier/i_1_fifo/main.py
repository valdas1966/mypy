from f_search.ds.frontier.i_0_base.main import FrontierBase, State  
from collections import deque
from typing import Iterator, Iterable


class FrontierFifo(FrontierBase[State]):
    """
    ============================================================================
     FIFO Frontier implementation using a FIFO Queue.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self) -> None:
        """
        ========================================================================
         Init with an empty Frontier.
        ========================================================================
        """
        self._queue: deque[State] = deque()
        self._set: set[State] = set()

    def push(self, state: State) -> None:
        """
        ========================================================================
         Push a State to the Frontier.
         Complexity: O(1)
        ========================================================================
        """
        self._queue.append(state)
        self._set.add(state)

    def pop(self) -> State:
        """
        ========================================================================
         Pop the first State from the Frontier.
         Complexity: O(1)
        ========================================================================
        """
        state = self._queue.popleft()
        self._set.remove(state)
        return state

    def peek(self) -> State:
        """
        ========================================================================
         Peek at the first State from the Frontier.
         Complexity: O(1)
        ========================================================================
        """
        return self._queue[0]

    def to_iterable(self) -> Iterable[State]:
        """
        ========================================================================
         Convert the Frontier's States into an Iterable of States.
         Complexity: O(n)
        ========================================================================
        """
        return self._queue

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of States in the Frontier.
         Complexity: O(1)
        ========================================================================
        """
        return len(self._queue)  

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the Frontier contains the State.
         Complexity: O(1)
        ========================================================================
        """
        return state in self._set  
