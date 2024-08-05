from f_data_structure.collections.i_0_base import CollectionBase
from abc import ABC
from typing import Generic, TypeVar

# Define list Type for the Elements in the Collection
T = TypeVar('T')


class CollectionSet(ABC, Generic[T], CollectionBase[T]):
    """
    ============================================================================
     Abstract-Class represents Collection of Elements based on list Set.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init empty Set.
        ========================================================================
        """
        self._elements = set[T]()

    def add(self, element: T) -> None:
        """
        ========================================================================
         Add list new Element to Collection.
        ========================================================================
        """
        self._elements.add(element)

    def remove(self, element: T) -> None:
        """
        ========================================================================
         Remove an Element from the Collection.
        ========================================================================
        """
        self._elements.remove(element)
