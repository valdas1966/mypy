from __future__ import annotations
from f_heuristic_search.nodes.i_0_has_cost import NodeHasCost


class NodeG(NodeHasCost):
    """
    ============================================================================
     Node with a weight value (W) and a cost value (G) from the start node.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeHasCost = None,
                 w: int = 1) -> None:
        NodeHasCost.__init__(self, name, parent)
        self._w = w
        self.update_g()

    @property
    # Return the Node's Weight.
    def w(self) -> int:
        return self._w

    @property
    # Return the Cost to reach the Node from the Start.
    def g(self) -> int:
        return self._g

    def cost(self) -> int:
        """
        ========================================================================
         Returns Node's Cost-Func (the highest G-Value the lowest Cost-Value).
        ========================================================================
        """
        return -self._g

    def is_better_parent(self, parent: NodeG) -> bool:
        """
        ========================================================================
         Return True if the given Parent offers a better path (lower G-Value).
        ========================================================================
        """
        return self.g > parent.g + self.w

    def update_g(self) -> None:
        """
        ========================================================================
         Calculate a Node's G-Value.
        ========================================================================
        """
        self._g = self.parent.g + self._w if self.parent else 0
