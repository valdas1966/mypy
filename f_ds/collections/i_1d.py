from typing import Generic, TypeVar, Iterator, Collection, Callable
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.iterable import Iterable
from abc import ABC
from f_utils import u_list

Item = TypeVar('Item')   # Type of Items in the Collection


class Collection1D(ABC, Generic[Item], Nameable, Iterable):
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
        Iterable[Item].__init__(self)
        if items is None:
            items = list[Item]()
        self._items: Collection[Item] = items

    def filter(self, predicate: Callable[[Item], True]) -> list[Item]:
        """
        ========================================================================
         Return List of Items that met the Predicate.
        ========================================================================
        """
        return u_list.to_filter(li=list(self), predicate=predicate)

    def sample(self,
               pct: int = None,
               size: int = None,
               predicate: Callable[[Item], True] = None) -> list[Item]:
        """
        ========================================================================
         Return Sample List of Items by Pct/Size and Predicate.
        ========================================================================
        """
        return u_list.to_sample(li=list(self),
                                pct=pct,
                                size=size,
                                predicate=predicate)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Collection.
         Ex: Name([...])
        ========================================================================
        """
        if self._items is None:
            return f'{self.name}(None)'
        return f'{self.name}({list(self)})'

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iterating over the Items.
        ========================================================================
        """
        return iter(self._items)

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of Items in the Collection.
        ========================================================================
        """
        return len(self._items)

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the given Item is in the Collection.
        ========================================================================
        """
        return item in self._items
