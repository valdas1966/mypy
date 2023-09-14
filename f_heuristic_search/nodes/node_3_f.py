from __future__ import annotations
from f_heuristic_search.nodes.node_1_cell import NodeCell
from f_heuristic_search.nodes.node_2_g import NodeG
from f_heuristic_search.nodes.node_2_h import NodeH
from f_heuristic_search.alias.cell import Cell


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     1. Informed-Node representing its estimated location on the path between
         the Start and Goal nodes.
     2. While comparing two nodes, if they have the same f-value, the node with
        the higher g-value is considered 'lesser'. This is because the g-value
        provides a more reliable indication of path cost.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. name (str)               : Node's Name.
        2. row (int)                : Node's Row.
        3. col (int)                : Node's Col.
        4. parent (NodeG)           : Node's Parent.
        5. children (list[NodeG])   : Node's Children.
        6. w (int)                  : Node's Weight.
        7. g (int)                  : Cost from Start to Node.
        8. h (int)                  : Heuristic Cost from Node to Goal.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. f() -> int
           [*] Estimates cost of the Optimal-Path from Start to Goal via
                this Node.
    ============================================================================
     Class Methods:
    ----------------------------------------------------------------------------
        1. from_node_cell(node: NodeCell) -> NodeH
           [*] Converts NodeCell into NodeF.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodeF = None,
                 w: int = 1,
                 h: int = None
                 ) -> None:
        NodeG.__init__(self, name=name, cell=cell, parent=parent, w=w)
        NodeH.__init__(self, name=name, cell=cell, h=h)

    def f(self) -> int:
        """
        ========================================================================
         Estimates cost of the Optimal-Path from Start to Goal via this Node.
          It is used to prioritize nodes during search.
        ========================================================================
        """
        return self.g + self.h

    def __lt__(self, other: NodeF) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() < other.f() or NodeG.__lt__(self, other)

    def __le__(self, other: NodeF) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() <= other.f() or NodeG.__le__(self, other)

    def __gt__(self, other: NodeF) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() > other.f() or NodeG.__gt__(self, other)

    def __ge__(self, other: NodeF) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() >= other.f() or NodeG.__ge__(self, other)

    @classmethod
    def from_node_cell(cls, node: NodeCell) -> NodeF:
        """
        ========================================================================
         Converts from NodeCell into NodeF.
        ========================================================================
        """
        return cls(name=node.name,
                   cell=node.cell,
                   parent=node.parent)
