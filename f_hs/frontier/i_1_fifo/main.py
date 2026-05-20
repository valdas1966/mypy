from collections import deque
from f_hs.frontier.i_0_base.main import FrontierBase
from typing import Any, Generic, Hashable, Iterator, TypeVar

State = TypeVar('State', bound=Hashable)


class FrontierFIFO(Generic[State], FrontierBase[State]):
    """
    ============================================================================
     FIFO Frontier (First-In-First-Out).
     Deque for order + auxiliary set for O(1) membership check.
     Priority is accepted for interface symmetry but ignored.

     Inherits the 3-counter scaffold from `FrontierBase`. Only
     `cnt_push` and `cnt_pop` are incremented — `decrease` is a
     no-op on FIFO and does not increment `cnt_decrease`
     (counts reflect what the frontier actually did, not what
     was called).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        FrontierBase.__init__(self)
        self._queue: deque[State] = deque()
        self._members: set[State] = set()

    def push(self,
             state: State,
             priority: Any = None) -> None:
        """
        ========================================================================
         Append State to the back of the queue (priority ignored).
        ========================================================================
        """
        self._counters.inc('cnt_push')
        self._queue.append(state)
        self._members.add(state)
        self._track_max_size()

    def pop(self) -> State:
        """
        ========================================================================
         Pop the State from the front of the queue.
        ========================================================================
        """
        self._counters.inc('cnt_pop')
        state = self._queue.popleft()
        self._members.discard(state)
        return state

    def clear(self) -> None:
        """
        ========================================================================
         Remove all States from the Frontier. Does NOT reset
         the counters — they accumulate over the whole run.
        ========================================================================
        """
        self._queue.clear()
        self._members.clear()

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the State is in the Frontier.
        ========================================================================
        """
        return state in self._members

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Frontier is not empty.
        ========================================================================
        """
        return len(self._queue) > 0

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of States in the Frontier.
        ========================================================================
        """
        return len(self._queue)

    def __iter__(self) -> Iterator[State]:
        """
        ========================================================================
         Iterate over States in FIFO order.
        ========================================================================
        """
        return iter(self._queue)
