from f_core.mixins import Dictable
from f_search.state import State
from f_search.cost import Cost


class Generated(Dictable[State, Cost]):
    """
    ============================================================================
     Priority-Queue of Generated-States implemented as a Dictionary.
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
        Dictable.__init__(self)

    def push(self, state: State, cost: Cost) -> None:
        """
        ========================================================================
         Push a new State into the Generated Queue.
         O(1) time complexity.
        ========================================================================
        """
        self._data[state] = cost

    def pop(self) -> State:
        """
        ========================================================================
         Pop the State with the lowest Cost from the Generated Queue.
         O(n) time complexity.
        ========================================================================
        """
        item_lowest = min(self._data, key=self._data.get)
        del self._data[item_lowest]
        return item_lowest
