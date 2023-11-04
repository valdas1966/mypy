from __future__ import annotations
from f_data_structure.nodes.node_1_hierarchical import NodeHierarchical
from f_data_structure.nodes.node_1_has_cost import NodeHasCost


class NodeG(NodeHierarchical, NodeHasCost):
    """
    ============================================================================
     Node with a weight value (W) and a cost value (G) from the start node.
    ==========================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. is_better_parent(parent: NodeG) -> bool
           [*] Returns True if the given Parent has a lower G-Value than the
                current one.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        # Hierarchical
    ----------------------------------------------------------------------------
        1. path_from_ancestor(other: NodeG) -> list[NodeG]
          [*] Returns a Path from a given Node to the Current.
    ----------------------------------------------------------------------------
        # NodeHasCost
    ----------------------------------------------------------------------------
        1. cost() -> int
           [*] Returns the Negative-G (the highest G, the lowest Cost).
    ============================================================================
     Inherited Magic Methods:
    ----------------------------------------------------------------------------
        # NameAble
    ----------------------------------------------------------------------------
        1. str() -> str
        2. repr() -> str
    ----------------------------------------------------------------------------
        # HasCost
    ----------------------------------------------------------------------------
        3. eq() -> bool
        4. ne() -> bool
        5. lt() -> bool
        6. le() -> bool
        7. gt() -> bool
        8. ge() -> bool
    ============================================================================
    """

    name:     str           # Node's Name
    parent:   NodeG         # Node's Parent
    children: list[NodeG]   # Node's Children
    w:        int           # Node's Weight
    g:        int           # Cost to reach the Node from the Start

    def __init__(self,
                 name: str = None,
                 parent: NodeG = None,
                 w: int = 1
                 ) -> None:
        NodeHierarchical.__init__(self, name=name, parent=parent)
        NodeHasCost.__init__(self, name=name)
        self._w = w
        self._calc_g()

    @property
    def w(self) -> int:
        return self._w

    @property
    def g(self) -> int:
        return self._g

    @NodeHierarchical.parent.setter
    def parent(self, parent: NodeG) -> None:
        """
        ========================================================================
         Sets a new Parent and updates the G-Value accordingly.
        ========================================================================
        """
        NodeHierarchical.parent.fset(self, parent)
        self._calc_g()

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
         Returns True if the given Parent is better than the current
         (lower G-Value).
        ========================================================================
        """
        return self.g > parent.g + self.w

    def _calc_g(self) -> None:
        """
        ========================================================================
         Updates Node's G-Value.
        ========================================================================
        """
        self._g = self.parent.g + self._w if self.parent else 0
