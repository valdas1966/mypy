from collections.abc import Collection
from f_core.mixins.sizable import Sizable
from typing import TypeVar, Generic, Iterator, Iterable, Sized, Protocol
from abc import abstractmethod

Item = TypeVar('Item')


class IterableSized(Protocol, Iterable, Sized):
    pass


class Collectionable(Generic[Item], Collection[Item], Sizable):
    """
    ============================================================================
     Mixin-Class for Objects with Collection functionality.
    ============================================================================
    """

    # Factory
    Factory: type = None

    @abstractmethod
    def to_iterable(self) -> IterableSized[Item]:
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

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR as List.
        ========================================================================
        """
        return str(list(self.to_iterable()))


