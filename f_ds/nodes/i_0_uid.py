from __future__ import annotations
from f_core.mixins.has_uid import HasUID
from f_core.mixins.has_name import HasName
from typing import Generic, TypeVar

UID = TypeVar('UID')


class NodeUid(Generic[UID], HasUID[UID], HasName):
    """
    ============================================================================
     ABC of Node classes.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasUID.__init__(self, uid=uid)
        HasName.__init__(self, name=name)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by Cell.
        ========================================================================
        """
        return HasUID.key_comparison(self)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Repr of the Node.
        ========================================================================
        """
        return f'{HasName.__str__(self)}({self._uid})'

    def __eq__(self, other: NodeUid) -> bool:
        """
        ========================================================================
         Return True if Node's Uid is equals to other Node's Uid.
        ========================================================================
        """
        return self.uid == other.uid

    def __ne__(self, other: NodeUid) -> bool:
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
    