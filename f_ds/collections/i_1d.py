from typing import Generic, TypeVar, Iterator, Collection
from f_abstract.mixins.nameable import Nameable
from abc import ABC
import random

Item = TypeVar('Item')   # Type of Items in the Collection


class Collection1D(ABC, Generic[Item], Nameable):
    """
    ============================================================================
     Abstract-Class represents a Collection of Items.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 items: Collection[Item] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        if items is None:
            items = list[Item]()
        self._items: Collection[Item] = items

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return a List of Items in the Collection.
        ========================================================================
        """
        return list(self._items)

    def random_by_size(self, size: int) -> list[Item]:
        """
        ========================================================================
         Return List of Random-Items by Size (number of items).
        ========================================================================
        """
        return random.sample(self.to_list(), k=size)

    def random_by_pct(self, pct: int) -> list[Item]:
        """
        ========================================================================
         Return List of Random-Items by Percentage (relative to len(self)).
        ========================================================================
        """
        size = int(pct * len(self) / 100)
        return self.random_by_size(size=size)

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the Item is in the Collection.
        ========================================================================
        """
        if not self._items:
            return False
        return item in self._items

    def __len__(self) -> int:
        """
        ========================================================================
         Return number of Items in the Collection.
        ========================================================================
        """
        return len(self._items)

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Collection is not Empty.
        ========================================================================
        """
        return bool(len(self))

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Collection.
         Ex: Name([...])
        ========================================================================
        """
        if self._items is None:
            return f'{self.name}(None)'
        return f'{self.name}({self.to_list()})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return Friendly-REPR.
         Ex: <Collection1D: Name([...])>
        ========================================================================
        """
        return f'<{self.__class__.__name__}: {str(self)}>'

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iterating over the Items.
        ========================================================================
        """
        return iter(self._items)
