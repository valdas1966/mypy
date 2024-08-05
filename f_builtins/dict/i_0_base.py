from abc import ABC
from typing import Generic, TypeVar, Iterator

K = TypeVar('K')   # Type for Keys
V = TypeVar('V')   # Type for Values


class DictBase(ABC, Generic[K, V], dict):
    """
    ============================================================================
     Abstract-Class for Dict-Based Collection.
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Init with an empty Dict.
        ========================================================================
        """
        dict().__init__()

    def add(self, key: K, value: V) -> None:
        """
        ========================================================================
        :param element:
        :return:
        """
        self[element] = None

    def remove(self, element: T) -> None:
        """
        Removes an element from the set. Raises KeyError if the element is not present.
        """
        super().pop(element)

    def __contains__(self, element: T) -> bool:
        """
        Checks if the set contains the specified element.
        """
        return element in self.keys()

    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator over the elements of the set in their insertion order.
        """
        return iter(self.keys())

    def __len__(self) -> int:
        """
        Returns the number of elements in the set.
        """
        return super().__len__()

    def __repr__(self) -> str:
        """
        Returns list string representation of the set.
        """
        elements = list(self.keys())
        return f'{self.__class__.__name__}({elements})'
