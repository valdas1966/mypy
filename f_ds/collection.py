from typing import Generic, TypeVar, Iterator, Collection
from abc import ABC

Item = TypeVar('Item')   # Type of Items in the Collection


class CollectionBase(ABC, Generic[Item]):
    """
    ============================================================================
     Abstract-Class represents a Collection of Items.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._items: Collection[Item] = None

    def items(self) -> list[Item]:
        """
        ========================================================================
         Return a List of Items in the Collection.
        ========================================================================
        """
        return list(self._items)

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the Item is in the Collection.
        ========================================================================
        """
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
        return bool(self.__len__())

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Collection.
        ========================================================================
        """
        return f'{self.__class__.__name__}({self.items()})'

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Item]:
        return iter(self._items)
