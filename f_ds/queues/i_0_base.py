from abc import abstractmethod
from typing import Generic, TypeVar
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.to_list import ToList, Listable

Item = TypeVar('Item')


class QueueBase(Generic[Item], ToList[Item], Nameable):
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
    def to_list(self) -> Listable[Item]:
        pass
