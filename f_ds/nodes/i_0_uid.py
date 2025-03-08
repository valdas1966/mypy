from f_core.mixins.has_key import HasKey
from f_core.mixins.has_name import HasName
from f_core.abstracts.clonable import Clonable
from typing import Generic, TypeVar

K = TypeVar('K')
Node = TypeVar('Node', bound='NodeUid')


class NodeUid(Generic[K], HasKey[K], HasName, Clonable):
    """
    ============================================================================
     ABC of Node classes.
    ============================================================================
    """

    def __init__(self,
                 key: K,
                 name: str = 'Node') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasKey.__init__(self, key=key)
        HasName.__init__(self, name=name)
        Clonable.__init__(self)

    def key_comparison(self) -> K:
        """
        ========================================================================
         Compare by Cell.
        ========================================================================
        """
        return HasKey.key_comparison(self)
    
    def clone(self) -> Node:
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
        return f'{HasName.__str__(self)}({self._uid})'


    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by UID.
        ========================================================================
        """
        return HasUID.__hash__(self)
    