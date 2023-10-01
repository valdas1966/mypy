from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.parentable import Parentable


class NodeBase(Nameable, Parentable):
    """
    ============================================================================
     Base Node-Class.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. path_from(other: NodeBase) -> list[NodeBase]
          [*] Returns a Path from a given Node to the Current.
    ============================================================================
    """

    _name: str                       # Node's Name
    _parent: NodeBase                # Node's Parent
    _children: list[NodeBase]        # Node's Children

    def __init__(self,
                 name: str = None,
                 parent: NodeBase = None) -> None:
        Nameable.__init__(self, name)
        Parentable.__init__(self, parent)

    def path_from(self, other: NodeBase) -> list[NodeBase]:
        """
        ========================================================================
         Returns a Path from a given Node to the Current.
        ========================================================================
        """
        if self == other:
            return [self]
        path = [self]
        current = self.parent
        while current and not current == other:
            path.append(current)
            current = current.parent
        # if path not found
        if not current:
            return list()
        path.append(other)
        path.reverse()
        return path
