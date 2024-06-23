from __future__ import annotations
from f_abstract.mixins.sortable import Sortable
from f_abstract.mixins.printable import Printable


class Nameable(Sortable, Printable):
    """
    ============================================================================
     Mixin with a Name property (Default=None).
    ============================================================================
    """

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

    def key_comparison(self) -> list:
        """
        ========================================================================
         Returns the Object's Key for Sorting.
        ========================================================================
        """
        return [self._name or str()]

    def __str__(self) -> str:
        """
        ========================================================================
         Return object string representation.
        ========================================================================
        """
        return self.name or 'None'

    def __hash__(self) -> int:
        """
        ========================================================================
         Return a Hash-Value of the object's name.
        ========================================================================
        """
        return hash(self.name)
