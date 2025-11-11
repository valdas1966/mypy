from f_ds.mixins.collectionable import Collectionable
from f_core.mixins.comparable import Comparable
from f_search.ds.state import State
from typing import Self, Iterable


class Path(Collectionable[State],
           Comparable):
    """
    ========================================================================
     Path of States in Search-Space.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, states: Iterable[State] = None) -> None:
        """
        ========================================================================
         Initialize the Path.
        ========================================================================
        """
        self._states: list[State] = list(states) if states else list()

    def to_iterable(self) -> list[State]:
        """
        ========================================================================
         Convert the Path to a list of States.
        ========================================================================
        """
        return self._states

    def head(self) -> State:
        """
        ========================================================================
         Get the head state.
        ========================================================================
        """
        return self._states[0]
    
    def tail(self) -> State:
        """
        ========================================================================
         Get the tail state.
        ========================================================================
        """
        return self._states[-1]
    
    def reverse(self) -> Self:
        """
        ========================================================================
         Return a reversed copy of the Path.
        ========================================================================
        """
        rev = reversed(self._states)
        return type(self)(states=list(rev))

    def key_comparison(self) -> list[State]:
        """
        ========================================================================
         Return the key comparison of the Path.
        ========================================================================
        """
        return self._states

    def __add__(self, other: Self) -> Self:
        """
        ========================================================================
         Add two Paths.
        ========================================================================
        """
        return type(self)(states=self._states + other._states)

    def __iadd__(self, other: Self) -> Self:
        """
        ========================================================================
         Add two Paths.
        ========================================================================
        """
        self._states += other._states
        return self
