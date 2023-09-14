from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.parentable import Parentable


class NodeBase(Nameable, Parentable):
    """
    ============================================================================
     Base General Node-Class.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. name (str)                    : Node's Name.
        2. children (list[NodeBase])     : Node's Children.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeBase = None,
                 children: list[NodeBase] = list()) -> None:
        Nameable.__init__(self, name)
        Parentable.__init__(self, parent, children)
