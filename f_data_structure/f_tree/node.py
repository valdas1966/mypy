from __future__ import annotations
from typing import Iterable
from anytree import NodeMixin
from f_abstract.mixins.nameable import Nameable



class Node(Nameable, NodeMixin):
    """
    ============================================================================
     Node in a Tree.
    ============================================================================
     Inherited Magic-Methods:
    ----------------------------------------------------------------------------
        1. [Nameable] str() -> str
        2. [Nameable] repr() -> str
    ============================================================================
    """

    # Nameable
    name: str                        # Node's Name
    # NodeMixin
    parent: NodeMixin                # Node's Parent
    children: Iterable[NodeMixin]    # Node's Children

    def __init__(self, name: str = None, parent: Node = None) -> None:
        """
        ========================================================================
         Initializes the base classes.
        ========================================================================
        """
        NodeMixin.__init__(self)
        Nameable.__init__(self, name=name)
        self.parent = parent
