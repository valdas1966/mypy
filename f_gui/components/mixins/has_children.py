from __future__ import annotations
from f_ds.nodes.i_1_children import NodeChildren


class HasChildren(NodeChildren):
    """
    ============================================================================
    
    """

    def __init__(self, key: str) -> None:
        """
        ========================================================================
         Initialize the HasChildren.
        ========================================================================
        """
        NodeChildren.__init__(self, key=key)

    def add_child(self, child: HasChildren) -> None:
        """
        ========================================================================
         Add a child to the HasChildren.
        ========================================================================
        """
        NodeChildren.add_child(self, child=child)
        child.parent = self

