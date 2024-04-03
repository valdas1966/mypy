from __future__ import annotations
from f_data_structure.nodes.i_1_path import NodePath


class NodeG(NodePath):
    """
    ============================================================================
     Node with a weight value (W) and a cost value (G) from the start node.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeG = None,
                 w: int = 1) -> None:
        NodePath.__init__(self, name=name, parent=parent)
        self._w: int = w
        self._g: int = 0
        self._update_g()

    @property
    # Return the Node's Weight.
    def w(self) -> int:
        return self._w

    @property
    # Return the Cost to reach the Node from the Start.
    def g(self) -> int:
        return self._g

    def _update_g(self) -> None:
        """
        ========================================================================
         Update the Node's G-value (Cost from the start node to this node).
        ========================================================================
        """
        self._g = self.parent.g + self._w if self.parent else 0

    def update_parent_if_needed(self, parent: NodeG) -> None:
        """
        ========================================================================
         Update Node's Parent if it offers a lower G-Value.
        ========================================================================
        """
        if self.g > parent.g + self.w:
            self.update_parent(parent)

    def update_parent(self, parent: NodeG) -> None:
        """
        ========================================================================
         Update Node's Parent and G-Value consequently.
        ========================================================================
        """
        self.parent = parent
        self._update_g()

    def key_comparison(self) -> list[int]:
        """
        ========================================================================
         Returns Node's Cost-Func (highest G-Value = lowest Cost).
        ========================================================================
        """
        return [-self._g]
