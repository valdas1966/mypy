from f_abstract.mixins.printable import Printable
from typing import Generic, TypeVar, Iterator
from collections.abc import Iterable as ABCIterable, Sized, Container
from abc import abstractmethod

Item = TypeVar('Item')


class Iterable(Generic[Item], Printable, ABCIterable, Sized, Container):
    """
    ============================================================================
     Mixin-Class for Iterable objects.
    ============================================================================
    """

    @abstractmethod
    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return a list representation of the Object.
        ========================================================================
        """
        pass

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Return an Iterator to iterate over the Object.
        ========================================================================
        """
        return iter(self.to_list())

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of Items in the Object.
        ========================================================================
        """
        return len(self.to_list())

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Object is not Empty.
        ========================================================================
        """
        return bool(len(self))

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the given Item is in the Object.
        ========================================================================
        """
        return item in self.to_list()

    def __str__(self) -> str:
        """
        ========================================================================
         Return string representation of the Object.
        ========================================================================
        """
        return str(self.to_list())
