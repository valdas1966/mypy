from collections.abc import Collection
from f_abstract.mixins.sizable import Sizable
from typing import TypeVar, Generic, Iterator, Iterable, Sized
from abc import abstractmethod

Item = TypeVar('Item')


class Collectionable(Generic[Item], Collection[Item], Sizable):
    """
    ============================================================================
     Mixin-Class for Objects with Collection functionality.
    ============================================================================
    """

    @abstractmethod
    def to_iterable(self) -> Iterable[Item] & Sized:
        """
        ========================================================================
         Convert the Object's Items into a List.
        ========================================================================
        """
        pass

    def __len__(self) -> int:
        """
        ========================================================================
         Return the Length of the Object's Items.
        ========================================================================
        """
        return len(self.to_iterable())

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the Object contains a received Item.
        ========================================================================
        """
        return item in self.to_iterable()

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iteration over the Object's Items.
        ========================================================================
        """
        return iter(self.to_iterable())
