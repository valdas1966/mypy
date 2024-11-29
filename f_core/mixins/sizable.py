from collections.abc import Sized
from abc import abstractmethod


class Sizable(Sized):
    """
    ============================================================================
     Mixin-Class for Sizable objects.
    ============================================================================
    """

    @abstractmethod
    def __len__(self) -> int:
        """
        ========================================================================
         Return the Object's Length.
        ========================================================================
        """
        pass

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Object is not Empty.
        ========================================================================
        """
        return bool(len(self))
