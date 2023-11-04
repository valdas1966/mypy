from __future__ import annotations
from f_data_structure.nodes.node_1_hierarchical import NodeHierarchical
from f_data_structure.nodes.node_1_has_cost import NodeHasCost


class NodeH(NodeHierarchical, NodeHasCost):
    """
    ============================================================================
     Node with a H-Value (Heuristic cost for reaching the Goal).
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
           [*] Returns the H-Value.
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

    name: str                  # Node's Name
    parent: NodeH              # Node's Parent
    children: list[NodeH]      # Node's Children
    h: int                     # Heuristic-Cost for reaching the Goal

    def __init__(self,
                 name: str = None,
                 parent: NodeH = None,
                 h: int = None
                 ) -> None:
        NodeHierarchical.__init__(self, name=name, parent=parent)
        NodeHasCost.__init__(self, name=name)
        self._h = h

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, h_new: int) -> None:
        self._h = h_new

    def cost(self) -> int:
        """
        ========================================================================
         Returns Node's Cost-Func (the H-Value).
        ========================================================================
        """
        return self.h
