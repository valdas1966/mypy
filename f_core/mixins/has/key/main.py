from f_core.mixins.comparable import Comparable
from f_core.mixins.hashable import Hashable
from f_core.mixins.has.repr import HasRepr
from typing import Generic, TypeVar

Key = TypeVar('Key')


class HasKey(Comparable, Hashable, HasRepr, Generic[Key]):
    """
    ============================================================================
     Mixin for objects that have a key.
    ============================================================================
    """ 

    # Factory
    Factory: type | None = None

    def __init__(self, key: Key) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key

    @property
    def key(self) -> Key:
        """
        ========================================================================
         Return the key of the object.
        ========================================================================
        """ 
        return self._key

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the object.
        ========================================================================
        """
        return str(self.key)
