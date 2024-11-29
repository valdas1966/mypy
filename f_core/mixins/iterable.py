from f_core.mixins.printable import Printable
from typing import Generic, TypeVar, Iterator
from abc import abstractmethod

Item = TypeVar('Item')


class Iterable(Generic[Item], Printable):
    """
    ============================================================================
     Mixin-Class for Iterable objects.
    ============================================================================
    """

    @abstractmethod
    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return list representation of the Object.
        ========================================================================
        """
        pass

    def insert(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Insert an Item into a given Index.
        ========================================================================
        """
        list(self).insert(index, item)
        print(list(self))

    def move(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Move an Item to a given Index.
        ========================================================================
        """
        self.to_list().remove(item)
        self.insert(item=item, index=index)

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
         Return True if the Object contains the given Item.
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
