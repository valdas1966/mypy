from typing import Generic, TypeVar
from abc import ABC, abstractmethod

Item = TypeVar('Item')


class Listable(ABC, Generic[Item]):
    """
    ============================================================================
     Abstract class for all listable files.
    ============================================================================
    """
    
    @abstractmethod
    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Convert the file to a list.
        ========================================================================
        """
        pass
