from abc import abstractmethod
from typing import Generic, TypeVar
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.groupable import Groupable, Group

Item = TypeVar('Item')


class QueueBase(Generic[Item], Groupable[Item], Nameable):
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
    def to_group(self, name: str = None) -> Group[Item]:
        pass
