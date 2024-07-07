from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.parentable import Parentable


class NodeBase(Nameable, Parentable):
    """
    ============================================================================
     Node Base-Class.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeBase = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        Parentable.__init__(self, parent=parent)
