from __future__ import annotations
from f_abstract.mixins.sortable import Sortable


class Nameable(Sortable):
    """
    ============================================================================
     Mixin with a Name property (Default=None).
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
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
        return [self._name]

    def __str__(self) -> str:
        return self.name if self.name else 'None'

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {self.__str__()}>'

    def __hash__(self) -> int:
        return hash(self.name)
