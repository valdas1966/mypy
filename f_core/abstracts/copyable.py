from __future__ import annotations
from abc import ABC, abstractmethod


class Copyable(ABC):

    @abstractmethod
    def copy(self) -> Copyable:
        """
        ========================================================================
         Return a Copy of the object.
        ========================================================================
        """

    def __copy__(self) -> Copyable:
        """
        ========================================================================
         Return a Copy of the object.
        ========================================================================
        """
        return self.copy()
