from __future__ import annotations
from abc import ABC, abstractmethod


class Clonable(ABC):

    @abstractmethod
    def clone(self) -> Clonable:
        """
        ========================================================================
         Clone an Object.
        ========================================================================
        """
