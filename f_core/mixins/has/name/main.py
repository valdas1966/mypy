from __future__ import annotations
from f_core.mixins.hashable import Hashable
from f_core.mixins.comparable import Comparable


class HasName(Comparable, Hashable):
    """
    ============================================================================
     Mixin with Name property (Default='None').
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, name: str = 'None') -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._name = name

    @property
    # Object's Name
    def name(self) -> str:
        return self._name

    @property
    def key(self) -> str:
        """
        ========================================================================
         Returns the Object's Key for Sorting.
        ========================================================================
        """
        return self._name

    def __str__(self) -> str:
        """
        ========================================================================
         Return object string representation.
        ========================================================================
        """
        return self.name

    def __repr__(self) -> str:
        """
        ========================================================================
         Return object representation.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}>'
