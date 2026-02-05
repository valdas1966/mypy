from __future__ import annotations
from f_core.mixins.comparable import Comparable


class HasName(Comparable):
    """
    ============================================================================
     Mixin with list Name property (Default=None).
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self, name: str = None) -> None:
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

    @name.setter
    def name(self, name: str) -> None:
        """
        ========================================================================
         Set the Object's Name.
        ========================================================================
        """
        self._name = name

    def key_comparison(self) -> str:
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
        return self.name or 'None'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return object string representation.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}>'

    def __hash__(self) -> int:
        """
        ========================================================================
         Return Hash-Value of the object's name.
        ========================================================================
        """
        return hash(self.name)
