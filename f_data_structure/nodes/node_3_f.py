from __future__ import annotations
from f_data_structure.nodes.node_2_g import NodeG
from f_data_structure.nodes.node_2_h import NodeH


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     1. Informed-Node representing its estimated location on the path between
         the Start and Goal nodes.
     2. While comparing two nodes, if they have the same f-value, the node with
         the higher g-value is considered 'lesser'. This is because the g-value
         provides a more reliable indication of path cost.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. f() -> int
           [*] Estimates the cost of the optimal path from the start node to
                the goal node through this Node.
        2. cost() -> int [Override NodeG and NodeH]
           [*] Return Node's Cost-Func by f() and NodeG.cost() on Tie-Breaking.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        # Hierarchical
    ----------------------------------------------------------------------------
        1. path_from_ancestor(other: Hierarchical) -> list[Hierarchical]
          [*] Returns a Path from an other Node to the Current.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. Comparison funcs based on f() with Tie-Breaking.

    ============================================================================
    """

    name: str                      # Node's Name
    parent: NodeG                  # Node's Parent
    children: list[NodeF]          # Node's Children
    g: int                         # Cost to reach the Node from the Start
    h: int                         # Heuristic cost for reaching the Goal.

    def __init__(self,
                 name: str = None,
                 parent: NodeF = None,
                 h: int = None
                 ) -> None:
        NodeG.__init__(self, name=name, parent=parent)
        NodeH.__init__(self, name=name, parent=parent, h=h)

    def f(self) -> int:
        """
        ========================================================================
         1. Estimates the cost of the optimal path from the start node to the
             goal node through this Node.
         2. This estimate is used to prioritize nodes during the search.
        ========================================================================
        """
        return self.g + self.h

    def cost(self) -> int:
        """
        ========================================================================
         Return Node's Cost-Func by f() and NodeG.cost() on Tie-Breaking.
        ========================================================================
        """
        return self.f(), NodeG.cost()
