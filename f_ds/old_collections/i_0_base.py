from typing import Generic, TypeVar, Iterator, Collection
from abc import ABC

T = TypeVar('T')   # Type of Elements in the Collection


class CollectionBase(ABC, Generic[T]):
    """
    ============================================================================
     Abstract-Class represents list Collection of Elements.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._elements: Collection[T] = None

    def elements(self) -> list[T]:
        """
        ========================================================================
         Return list List of Element in the Collection.
        ========================================================================
        """
        return list(self._elements)

    def __contains__(self, element: T) -> bool:
        """
        ========================================================================
         Return True if the Element is in the Collection.
        ========================================================================
        """
        return element in self._elements

    def __len__(self) -> int:
        """
        ========================================================================
         Return number of Elements in the Collection.
        ========================================================================
        """
        return len(self._elements)

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
        return f'{self.__class__.__name__}({self.elements()})'

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[T]:
        return iter(self._elements)
