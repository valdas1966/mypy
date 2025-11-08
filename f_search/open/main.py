from f_ds.queues.i_1_priority.main import QueuePriority, Item, Priority
from f_core.mixins.sizable import Sizable
from typing import Generic, Iterable
from enum import Enum


class PolicyOpen(Enum):
    PRIORITY = 'PRIORITY'


class Open(Generic[Item, Priority], Sizable):
    """
    ============================================================================
     Open List for storing Items with Priorities.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 policy: PolicyOpen = PolicyOpen.PRIORITY) -> None:
        """
        ========================================================================
         Initialize the Open list with the appropriate policy.
        ========================================================================
        """
        if policy == PolicyOpen.PRIORITY:
            self._queue = QueuePriority[Item, Priority]()

    def push(self,
             item: Item,
             priority: Priority=None) -> None:
        """
        ========================================================================
         Push an Item into the Open List.
        ========================================================================
        """
        self._queue.push(item=item, priority=priority)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Item from the Open List.
        ========================================================================
        """
        return self._queue.pop()

    def peek(self) -> Item:
        """
        ========================================================================
         Peek at the next Item in the Open List.
        ========================================================================
        """
        return self._queue.peek()

    def to_iterable(self) -> Iterable[Item]:
        """
        ========================================================================
         Return the Open List as an Iterable.
        ========================================================================
        """
        return self._queue.to_iterable()

    def __len__(self) -> int:
        """
        ========================================================================
         Return the size of the Open List.
        ========================================================================
        """
        return len(self._queue)
