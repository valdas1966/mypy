from f_ds.queues.i_1_indexed import QueueIndexed
from f_hs.frontier.i_0_base.main import FrontierBase
from typing import Any, Generic, Hashable, Iterator, TypeVar

State = TypeVar('State', bound=Hashable)


class FrontierPriority(Generic[State], FrontierBase[State]):
    """
    ============================================================================
     Priority Frontier backed by an indexed min-heap (QueueIndexed).
     Each State appears at most once. O(log n) push, pop, decrease.
     Used by A* and Dijkstra.
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
        self._queue: QueueIndexed[State, Any] = QueueIndexed()

    def push(self,
             state: State,
             priority: Any = None) -> None:
        """
        ========================================================================
         Push a State with the given Priority.
         If the State already exists, decrease its key if better.
        ========================================================================
        """
        self._queue.push(item=state, priority=priority)

    def pop(self) -> State:
        """
        ========================================================================
         Pop the State with the lowest Priority.
        ========================================================================
        """
        return self._queue.pop()

    def decrease(self,
                 state: State,
                 priority: Any = None) -> None:
        """
        ========================================================================
         Decrease the Priority of an existing State.
         No-op if the new Priority is not better.
        ========================================================================
        """
        self._queue.decrease_key(item=state, priority=priority)

    def clear(self) -> None:
        """
        ========================================================================
         Remove all States from the Frontier.
        ========================================================================
        """
        self._queue.clear()

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the State is in the Frontier.
        ========================================================================
        """
        return state in self._queue

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Frontier is not empty.
        ========================================================================
        """
        return bool(self._queue)

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
         Iterate over States in the Frontier. Order is heap-
         internal (not priority-sorted). Used by
         `AlgoSPP.refresh_priorities` to drain-and-rebuild.
        ========================================================================
        """
        return iter(self._queue.to_iterable())
