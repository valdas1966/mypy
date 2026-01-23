from f_core.mixins import Comparable
from typing import Generic, TypeVar

Key = TypeVar('Key')


class PriorityKey(Generic[Key], Comparable):
    """
    ============================================================================
     Priority based on the Key of a State.
    ============================================================================
    """

    def __init__(self, key: Key) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key

    def key_comparison(self) -> Key:
        """
        ========================================================================
         Return the Key of the State.
        ========================================================================
        """
        return self._key

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the string representation of the PriorityKey.
        ========================================================================
        """
        return f'PriorityKey(key={self._key})'
