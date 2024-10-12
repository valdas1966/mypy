from abc import abstractmethod
from typing import Generic, TypeVar, Iterator
from collections.abc import Iterable
from f_abstract.mixins.nameable import Nameable

Item = TypeVar('Item')


class QueueBase(Generic[Item], Nameable, Iterable):
    """
    ============================================================================
     Abstract-Class of Queue.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)

    @abstractmethod
    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Element into the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Element from the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Allow iterate over the Queue-Objects.
        ========================================================================
        """
        pass
