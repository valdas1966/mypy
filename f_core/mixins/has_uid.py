from f_core.mixins.comparable import Comparable
from typing import Generic, TypeVar

UID = TypeVar('UID')


class HasUID(Generic[UID], Comparable):
    """
    ============================================================================
     Mixin for Classes with UID (Unique Identifier) property.
    ============================================================================
    """

    def __init__(self, uid: UID) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._uid = uid

    @property
    def uid(self) -> UID:
        """
        ========================================================================
         Return an ID property.
        ========================================================================
        """
        return self._uid

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by the UID.
        ========================================================================
        """
        return [self._uid]

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash the object by an UID.
        ========================================================================
        """
        return hash(self._uid)
