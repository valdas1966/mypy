from typing import Generic, TypeVar, Hashable, Iterable

Item = TypeVar('Item', bound=Hashable)
Priority = TypeVar('Priority')


class QueueIndexed(Generic[Item, Priority]):
    """
    ========================================================================
     Indexed Min-Heap with Decrease-Key.
     Each item appears at most once. Supports O(log n) push, pop,
     and decrease_key. Priorities are tuples compared lexicographically.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._heap: list[list] = []
        self._index: dict[Item, int] = {}

    def push(self, item: Item, priority: Priority) -> None:
        """
        ====================================================================
         Push an Item with the given Priority.
         If the Item already exists, decrease its key if better.
        ====================================================================
        """
        if item in self._index:
            self.decrease_key(item=item, priority=priority)
            return
        entry = [priority, item]
        self._heap.append(entry)
        pos = len(self._heap) - 1
        self._index[item] = pos
        self._sift_up(pos=pos)

    def pop(self) -> Item:
        """
        ====================================================================
         Pop the Item with the lowest Priority.
        ====================================================================
        """
        heap = self._heap
        last = heap.pop()
        if not heap:
            del self._index[last[1]]
            return last[1]
        top = heap[0]
        del self._index[top[1]]
        heap[0] = last
        self._index[last[1]] = 0
        self._sift_down(pos=0)
        return top[1]

    def peek(self) -> Item:
        """
        ====================================================================
         Return the Item with the lowest Priority without removing.
        ====================================================================
        """
        return self._heap[0][1]

    def decrease_key(self,
                     item: Item,
                     priority: Priority) -> None:
        """
        ====================================================================
         Decrease the Priority of an existing Item.
         No-op if the new priority is not better.
        ====================================================================
        """
        pos = self._index[item]
        if priority < self._heap[pos][0]:
            self._heap[pos][0] = priority
            self._sift_up(pos=pos)

    def clear(self) -> None:
        """
        ====================================================================
         Remove all Items.
        ====================================================================
        """
        self._heap.clear()
        self._index.clear()

    def to_iterable(self) -> Iterable[Item]:
        """
        ====================================================================
         Return Items in Priority Order.
        ====================================================================
        """
        sorted_heap = sorted(self._heap, key=lambda e: e[0])
        return [entry[1] for entry in sorted_heap]

    def __contains__(self, item: Item) -> bool:
        """
        ====================================================================
         Return True if the Item is in the Heap.
        ====================================================================
        """
        return item in self._index

    def __len__(self) -> int:
        """
        ====================================================================
         Return the number of Items.
        ====================================================================
        """
        return len(self._heap)

    def __bool__(self) -> bool:
        """
        ====================================================================
         Return True if the Heap is not empty.
        ====================================================================
        """
        return len(self._heap) > 0

    # ──────────────────────────────────────────────────
    #  Internal Heap Operations
    # ──────────────────────────────────────────────────

    def _sift_up(self, pos: int) -> None:
        """
        ====================================================================
         Sift an Entry up to restore Heap Property.
        ====================================================================
        """
        heap = self._heap
        index = self._index
        entry = heap[pos]
        while pos > 0:
            parent_pos = (pos - 1) >> 1
            parent = heap[parent_pos]
            if entry[0] < parent[0]:
                heap[pos] = parent
                index[parent[1]] = pos
                pos = parent_pos
            else:
                break
        heap[pos] = entry
        index[entry[1]] = pos

    def _sift_down(self, pos: int) -> None:
        """
        ====================================================================
         Sift an Entry down to restore Heap Property.
        ====================================================================
        """
        heap = self._heap
        index = self._index
        n = len(heap)
        entry = heap[pos]
        child_pos = 2 * pos + 1
        while child_pos < n:
            right_pos = child_pos + 1
            if (right_pos < n
                    and heap[right_pos][0] < heap[child_pos][0]):
                child_pos = right_pos
            child = heap[child_pos]
            if child[0] < entry[0]:
                heap[pos] = child
                index[child[1]] = pos
                pos = child_pos
                child_pos = 2 * pos + 1
            else:
                break
        heap[pos] = entry
        index[entry[1]] = pos
