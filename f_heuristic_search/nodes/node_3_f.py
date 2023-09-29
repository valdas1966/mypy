from __future__ import annotations
from f_heuristic_search.nodes.node_2_g import NodeG
from f_heuristic_search.nodes.node_2_h import NodeH


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     Informed-Node representing its estimated location on the path between
       the Start and Goal nodes.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. f() -> int
           [*] Estimates the cost of the optimal path from the start node to
                the goal node through this Node.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: NodeCell) -> int
           [*] Manhattan-Distance between the Nodes.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. Comparison funcs based on f() with Tie-Breaking.
            While comparing two nodes, if they have the same f-value, the node
            with the higher g-value is considered 'lesser'. This is because the
            g-value provides a more reliable indication of path cost.
    ============================================================================
    """

    _name: str                      # Node's Name
    _parent: NodeG                  # Node's Parent
    _children: list[NodeF]          # Node's Children
    _row: int                       # Node's Row
    _col: int                       # Node's Col
    _w: int                         # Node's Weight
    _g: int                         # Cost to reach the Node from the Start
    _h: int                         # Heuristic cost for reaching the Goal.

    def __init__(self,
                 row: int = 0,
                 col: int = None,
                 name: str = None,
                 parent: NodeF = None,
                 w: int = 1,
                 h: int = None
                 ) -> None:
        NodeG.__init__(self, row=row, col=col, name=name, parent=parent, w=w)
        NodeH.__init__(self, row=row, col=col, name=name, parent=parent, h=h)

    def f(self) -> int:
        """
        ========================================================================
         1. Estimates the cost of the optimal path from the start node to the
             goal node through this Node.
         2. This estimate is used to prioritize nodes during the search.
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


node = NodeF()
s = {node}
print(node in s)