from f_core.mixins.has_uid import HasUID
from f_core.mixins.has_name import HasName
from f_core.abstracts.clonable import Clonable
from typing import Generic, TypeVar

UID = TypeVar('UID')
Node = TypeVar('Node', bound='NodeUid')


class NodeUid(Generic[UID], HasUID[UID], HasName, Clonable):
    """
    ============================================================================
     ABC of Node classes.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 name: str = 'Node') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasUID.__init__(self, uid=uid)
        HasName.__init__(self, name=name)
        Clonable.__init__(self)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by Cell.
        ========================================================================
        """
        return HasUID.key_comparison(self)
    
    def clone(self) -> Node:
        """
        ========================================================================
         Clone the Node.
        ========================================================================
        """
        uid = self.uid.clone() if isinstance(self.uid, Clonable) else self.uid
        return self.__class__(uid=uid, name=self.name)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Repr of the Node.
        ========================================================================
        """
        return f'{HasName.__str__(self)}({self._uid})'

    def __eq__(self, other: Node) -> bool:
        """
        ========================================================================
         Return True if Node's Uid is equals to other Node's Uid.
        ========================================================================
        """
        return self.uid == other.uid

    def __ne__(self, other: Node) -> bool:
        """
        ========================================================================
         Return True if Node's Uid is not equals to other Node's Uid.
        ========================================================================
        """
        return not self == other

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by UID.
        ========================================================================
        """
        return HasUID.__hash__(self)
    