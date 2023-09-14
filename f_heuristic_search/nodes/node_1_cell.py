from __future__ import annotations
from f_heuristic_search.nodes.node_0_base import NodeBase
from f_heuristic_search.alias.cell import Cell


class NodeCell(NodeBase, Cell):
    """
    ============================================================================
     Node representing a Cell in a 2D-Grid.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. name (str)                         : Node's Name.
        2. row (int)                          : Node's Row.
        3. col (int)                          : Node's Col.
        4. parent (NodeCell)                  : Node's Parent.
        5. children (list[NodeCell])         : Node's Children.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: NodeCell) -> int
           [*] Manhattan-Distance between the Nodes.
    ============================================================================
    """

    def __init__(self,
                 row: int,
                 col: int = None,
                 name: str = None,
                 parent: NodeCell = None) -> None:
        NodeBase.__init__(self, name=name, parent=parent)
        Cell.__init__(self, name=name, row=row, col=col)

    def children(self) -> list[NodeCell]:
        """
        ========================================================================
         Returns Children-Nodes (converts neighbors to Nodes beside the parent).
        ========================================================================
        """
        res = list()
        for neighbor in self.neighbors():
            if neighbor == self.parent:
                continue
            child = self.__class__(row=self.row, col=self.col)
            res.append(child)
        return res
