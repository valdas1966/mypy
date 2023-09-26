from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.parentable import Parentable


class NodeBase(Nameable, Parentable):
    """
    ============================================================================
     Base Node-Class.
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
