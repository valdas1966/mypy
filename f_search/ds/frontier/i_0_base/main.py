from f_ds.mixins.collectionable import Collectionable
from f_search.ds.state import StateBase
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

State = TypeVar('State', bound=StateBase)


class FrontierBase(ABC, Generic[State], Collectionable[State]):
    """
    ============================================================================
     Base for Frontier.
    ============================================================================
    """

    @abstractmethod
    def pop(self) -> State:
        """         
        ========================================================================
         Pop the best State from the Frontier.
        ========================================================================
        """
        pass

    @abstractmethod
    def peek(self) -> State:
        """
        ========================================================================
         Peek at the best State from the Frontier.
        ========================================================================
        """
        pass
