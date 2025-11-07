from f_core.mixins.has.key import HasKey
from f_core.mixins.has.name import HasName
from f_core.mixins.clonable import Clonable
from typing import Generic, TypeVar, Self


Key = TypeVar('Key')
Node = TypeVar('Node', bound='NodeKey')


class NodeKey(Generic[Key], HasKey[Key], HasName, Clonable):
    """
    ============================================================================
     ABC of Node classes.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 key: Key,
                 name: str = 'Node') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasKey.__init__(self, key=key)
        HasName.__init__(self, name=name)
        Clonable.__init__(self)

    def key_comparison(self) -> Key:
        """
        ========================================================================
         Compare by Cell.
        ========================================================================
        """
        return HasKey.key_comparison(self)
    
    def clone(self) -> Self:
        """
        ========================================================================
         Clone the Node.
        ========================================================================
        """
        # Clone the key if it is Clonable.
        key = self.key.clone() if isinstance(self.key, Clonable) else self.key
        # Return a new Node with the cloned key and name
        return self.__class__(key=key, name=self.name)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Repr of the Node.
        ========================================================================
        """
        return f'{self.name}({self.key})'
    
    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Key.
        ========================================================================
        """
        return HasKey.__hash__(self)
    