from abc import ABC, abstractmethod


class Printable(ABC):
    """
    ============================================================================
     Mixin-Class for Printable objects.
    ============================================================================
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        ========================================================================
         Return Object string representation.
        ========================================================================
        """
        pass

    def __repr__(self) -> str:
        """
        ========================================================================
         Return an informative Object Representation.
        ========================================================================
        """
        return f'<{type(self).__name__}: {str(self)}>'
