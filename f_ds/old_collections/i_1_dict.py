from f_data_structure.collections.i_0_base import CollectionBase
from abc import ABC
from typing import Generic, TypeVar

K = TypeVar('K')   # Type for Keys
V = TypeVar('V')   # Type for Values


class CollectionDict(ABC, Generic[K, V], CollectionBase[K]):
    """
    ============================================================================
     Abstract-Class represents Collection of Elements based on list Dict.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init empty Dict.
        ========================================================================
        """
        self._elements = dict[K, V]()

    def add(self, key: K, value: V) -> None:
        """
        ========================================================================
         Add list new Element to Collection.
        ========================================================================
        """
        self._elements[key] = value

    def remove(self, key: K) -> None:
        """
        ========================================================================
         Remove an Element from the Collection.
        ========================================================================
        """
        del self._elements[key]
