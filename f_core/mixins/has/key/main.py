from typing import Generic, TypeVar 
from f_core.mixins.comparable import Comparable

K = TypeVar('K')


class HasKey(Generic[K], Comparable):
    """
    ============================================================================
     Mixin for objects that have a key.
    ============================================================================
    """ 

    def __init__(self, key: K) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key
    
    @property
    def key(self) -> K:
        """
        ========================================================================
         Return the key of the object.
        ========================================================================
        """ 
        return self._key

    def key_comparison(self) -> K:
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