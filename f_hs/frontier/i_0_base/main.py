from typing import Any, Generic, Iterator, TypeVar

State = TypeVar('State')


class FrontierBase(Generic[State]):
    """
    ============================================================================
     Abstract Base for a Search Frontier.
     Holds candidate States awaiting expansion. Narrow interface:
     push, pop, decrease, contains, bool, len, iter, clear.
    ============================================================================
    """

    def push(self,
             state: State,
             priority: Any = None) -> None:
        """
        ========================================================================
         Push a State into the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def pop(self) -> State:
        """
        ========================================================================
         Pop and return the next State from the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def decrease(self,
                 state: State,
                 priority: Any = None) -> None:
        """
        ========================================================================
         Update the Priority of a State already in the Frontier.
         Default: no-op (for unpriorityed frontiers).
        ========================================================================
        """
        pass

    def clear(self) -> None:
        """
        ========================================================================
         Remove all States from the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the State is in the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Frontier is not empty.
        ========================================================================
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of States in the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[State]:
        """
        ========================================================================
         Iterate over States currently in the Frontier. Order is
         implementation-defined. Enables `list(frontier)` and
         callers (e.g., `AlgoSPP.refresh_priorities`) that need
         to visit all pending states.
        ========================================================================
        """
        raise NotImplementedError
