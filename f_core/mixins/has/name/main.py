from __future__ import annotations
from f_core.mixins.has.repr import HasRepr


class HasName(HasRepr):
    """
    ============================================================================
     Mixin with Name property (Default='None').
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, name: str = 'NoName') -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._name = name

    @property
    # Object's Name
    def name(self) -> str:
        """
        ========================================================================
         Return the object's name.
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

