from __future__ import annotations
from f_graph.path.node import NodePath


class NodeG(NodePath):
    """
    ============================================================================
     Mixin-Class for Nodes with G-Value (Cost from Start to current Node).
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeG = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodePath.__init__(self, name=name, parent=parent)
        self._g = (parent.g + 1) if parent else 0

    @property
    def g(self) -> int:
        """
        ========================================================================
         Cost from Start to current Node.
        ========================================================================
        """
        return self._g

    @NodePath.parent.setter
    def parent(self, parent_new: NodeG) -> None:
        """
        ========================================================================
         Set list new Parent and update the G-Value respectively.
        ========================================================================
        """
        self._parent = parent_new
        self._g = (parent_new.g + 1) if parent_new else 0

    def is_better_parent(self, parent_new: NodeG) -> bool:
        """
        ========================================================================
         Check if the new parent is better than the current based on G-Value.
        ========================================================================
        """
        return self._parent is None or (parent_new.g < self.parent.g)

    def key_comparison(self) -> list:
        """
        ========================================================================
         If F-Values are equal, break ties on H-Value.
        ========================================================================
        """
        return [-self.g, NodePath.key_comparison(self)]

    def __repr__(self) -> str:
        """
        ========================================================================
         '<NodeG: None> G=1'
        ========================================================================
        """
        return f'{NodePath.__repr__(self)} G={self.g}'
