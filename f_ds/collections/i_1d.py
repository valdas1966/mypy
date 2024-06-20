from typing import Generic, TypeVar, Iterator, Collection, Callable
from f_abstract.mixins.nameable import Nameable
from abc import ABC
from f_utils import u_list

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

    def filter(self, predicate: Callable[[Item], True]) -> list[Item]:
        """
        ========================================================================
         Return List of Items that met the Predicate.
        ========================================================================
        """
        return u_list.to_filter(li=self.to_list(), predicate=predicate)

    def sample(self,
               pct: int = None,
               size: int = None,
               predicate: Callable[[Item], True] = None) -> list[Item]:
        """
        ========================================================================
         Return Sample List of Items by Pct/Size and Predicate.
        ========================================================================
        """
        return u_list.to_sample(li=self.to_list(),
                                pct=pct,
                                size=size,
                                predicate=predicate)

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

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iterating over the Items.
        ========================================================================
        """
        return iter(self._items)
