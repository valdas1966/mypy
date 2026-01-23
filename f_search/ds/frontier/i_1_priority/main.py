from __future__ import annotations
from f_search.ds.frontier.i_0_base.main import FrontierBase, State
from f_search.ds.priority import PriorityKey
from typing import Generic, Iterable, TypeVar
import heapq

Priority = TypeVar('Priority', bound=PriorityKey)
HeapEntry = tuple[Priority, int, State]  # (priority, counter, state)


class FrontierPriority(Generic[State, Priority], FrontierBase[State]):
    """
    ============================================================================
     1. Priority Frontier optimized for A* search.
     2. Lazy deletion: Updates create new entries, old ones marked stale.
     3. Auto-compaction: Prevents heap bloat from priority updates.
     4. Counter: Ensures FIFO tie-breaking for stable ordering.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self) -> None:
        """
        ========================================================================
         Initialize empty frontier.
        ========================================================================
        """
        self._heap: list[HeapEntry] = []
        self._current: dict[State, tuple[Priority, int]] = {}
        self._counter: int = 0

    def push(self, state: State, priority: Priority) -> None:
        """
        ========================================================================
         1. Add a new state to the frontier.
         2. Precondition: state must NOT already be in frontier.
         3. For A*: only call when state is newly discovered.         
         4. Complexity: O(log n)
        ========================================================================
        """
        self._counter += 1
        cnt = self._counter
        self._current[state] = (priority, cnt)
        heapq.heappush(self._heap, (priority, cnt, state))

    def update(self, state: State, priority: Priority) -> None:
        """
        ========================================================================
         1. Update priority of existing state.
         2. Precondition: state must already be in frontier.
         3. For A*: only call when better path found (lower f-value).
         4. Creates new heap entry; old entry becomes stale and will be skipped.
         5. Complexity: O(log n)
        ========================================================================
        """
        self._counter += 1
        cnt = self._counter
        self._current[state] = (priority, cnt)
        heapq.heappush(self._heap, (priority, cnt, state))

    def pop(self) -> State:
        """
        ========================================================================
         1. Remove and return state with best (lowest) priority.
         2. Precondition: frontier must not be empty.
         3. Auto-compacts if heap has >3x current states (from stale updates).
         4. Skips stale entries until finding current best state.
         5. Complexity: O(log n) amortized
        ========================================================================
        """
        # Auto-compact if too many stale entries
        if len(self._heap) > 3 * len(self._current):
            self._compact()
        
        while True:
            priority, cnt, state = heapq.heappop(self._heap)
            cur = self._current.get(state)
            
            # Skip stale entries
            if cur is None:
                continue
                
            # Found current best
            if cur == (priority, cnt):
                del self._current[state]
                return state

    def peek(self) -> State:
        """
        ========================================================================
         1. Return state with best (lowest) priority without removing.
         2. Precondition: frontier must not be empty.
         3. Skips stale entries at heap top until finding current best.
         4. Complexity: O(1) amortized, O(k) worst case where k = stale entries
        ========================================================================
        """
        while True:
            priority, cnt, state = self._heap[0]
            cur = self._current.get(state)
            
            # Skip stale entries
            if cur is None or cur != (priority, cnt):
                heapq.heappop(self._heap)
                continue
                
            return state

    def _compact(self) -> None:
        """
        ========================================================================
         1. Remove all stale entries from heap.
         2. Called automatically by pop() when heap bloats.
         3. Rebuilds heap with only current states.
         4. Complexity: O(n log n)
        ========================================================================
        """
        new_heap: list[HeapEntry] = [
            (priority, cnt, state)
            for state, (priority, cnt) in self._current.items()
        ]
        heapq.heapify(new_heap)
        self._heap = new_heap

    def to_iterable(self) -> Iterable[State]:
        """
        ========================================================================
         1. Return iterable of all states currently in frontier.
         2. Order is arbitrary (not by priority).
         3. Complexity: O(1) - returns dict view
        ========================================================================
        """
        return self._current.keys()

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         1. Check if state is in frontier.
         2. Complexity: O(1)
        ========================================================================
        """
        return state in self._current

    def __len__(self) -> int:
        """
        ========================================================================
         1. Return number of states in frontier.
         2. Complexity: O(1)
        ========================================================================
        """
        return len(self._current)
