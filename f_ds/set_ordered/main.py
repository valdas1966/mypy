from collections.abc import MutableSet, Iterator, Iterable
from typing import TypeVar, Generic

Item = TypeVar('Item')


class SetOrdered(Generic[Item], MutableSet):
    """
    ========================================================================
     Set that preserves insertion order.
    ========================================================================
     Backed by a dict for O(1) add/discard/contains.
     Inherits full Set interface from MutableSet ABC.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, iterable: Iterable[Item] = None) -> None:
        """
        ====================================================================
         Init from an optional Iterable.
        ====================================================================
        """
        self._dict: dict[Item, None] = dict()
        if iterable:
            for item in iterable:
                self._dict[item] = None

    def add(self, item: Item) -> None:
        """
        ====================================================================
         Add an Item to the Set.
        ====================================================================
        """
        self._dict[item] = None

    def discard(self, item: Item) -> None:
        """
        ====================================================================
         Remove an Item from the Set (no error if absent).
        ====================================================================
        """
        self._dict.pop(item, None)

    def __contains__(self, item: object) -> bool:
        """
        ====================================================================
         Return True if the Item is in the Set.
        ====================================================================
        """
        return item in self._dict

    def __iter__(self) -> Iterator[Item]:
        """
        ====================================================================
         Iterate over Items in insertion order.
        ====================================================================
        """
        return iter(self._dict)

    def __len__(self) -> int:
        """
        ====================================================================
         Return the number of Items in the Set.
        ====================================================================
        """
        return len(self._dict)

    def __repr__(self) -> str:
        """
        ====================================================================
         Return STR-Representation (truncated for large Sets).
        ====================================================================
        """
        items = list(self._dict.keys())
        if len(items) <= 6:
            return f'SetOrdered({items})'
        head = ', '.join([str(item) for item in items[:3]])
        tail = items[-1]
        return f'SetOrdered({head}, ..., {tail}, len={len(items)})'
