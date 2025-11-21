from typing import Generic, TypeVar
from f_core.mixins.has.name import HasName

Key = TypeVar('Key')


class HasKey(Generic[Key], HasName):
    """
    ============================================================================
     Mixin for objects that have a key.
    ============================================================================
    """ 

    def __init__(self,
                 key: Key,
                 name: str = 'Key') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
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

    def __repr__(self) -> str:
        """
        ========================================================================
         Return object string representation.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}, Key={self.key}>'