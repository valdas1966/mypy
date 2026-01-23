from f_core.mixins import Comparable, Sizable
from f_search.ds.states import StateBase as State
from f_search.ds.priority import PriorityKey as Priority
from typing import Protocol, Iterator


class Frontier(Protocol[State], Sizable):
    """
    ============================================================================
     Protocol for a Frontier (Data-Structure for Generated-States).
    ============================================================================
    """

    def push(self, state: State, priority: Priority) -> None:
        """
        ========================================================================
         Push a State to the Frontier.
        ========================================================================
        """

    def pop(self) -> State:
        """
        ========================================================================
         Pop a State from the Frontier.
        ========================================================================
        """

    def __iter__(self) -> Iterator[State]:
        """
        ========================================================================
         Iterate over the Frontier.
        ========================================================================
        """
