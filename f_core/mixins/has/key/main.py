from typing import Generic, TypeVar 
from f_core.mixins.comparable import Comparable

Key = TypeVar('Key')


class HasKey(Generic[Key], Comparable):
    """
    ============================================================================
     Mixin for objects that have a key.
    ============================================================================
    """ 

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

    def key_comparison(self) -> Key:
        """
        ========================================================================
         Return the key of the object.
        ========================================================================
        """ 
        return self._key

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the hash of the object.
        ========================================================================
        """ 
        return hash(self._key)
