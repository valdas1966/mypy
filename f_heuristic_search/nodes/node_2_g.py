from __future__ import annotations
from f_abstract.mixins.parentable import Parentable
from f_heuristic_search.nodes.node_1_cell import NodeCell
from f_heuristic_search.alias.cell import Cell


class NodeG(NodeCell):
    """
    ============================================================================
     1. Node with a W-Value (Node's Weight) and a G-Value (Cost from the Start).
     2. The sorting is in opposite direction (the least NodeG is the Node with
         the largest G-Value, the farthest from the Start Node).
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
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. is_better_parent(parent: NodeG) -> bool
           [*] Returns True if the received Parent has a lower G-Value than the
                current one.
    ============================================================================
     Class Methods:
    ----------------------------------------------------------------------------
        1. from_node_cell(node: NodeCell) -> NodeG
           [*] Converts NodeCell into NodeG.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodeG = None,
                 w: int = 1
                 ) -> None:
        NodeCell.__init__(self, cell=cell, name=name, parent=parent)
        self._w = w
        self._g = 0 if parent is None else parent.g + self._w

    @property
    def w(self) -> int:
        return self._w

    @property
    def g(self) -> int:
        """
        ========================================================================
         Computes G-Value based on Cost from the Start-Node to the Parent-Node.
        ========================================================================
        """
        return self._g

    @Parentable.parent.setter
    def parent(self, parent: NodeG) -> None:
        """
        ========================================================================
         Sets new Parent and updates the G-Value respectively.
        ========================================================================
        """
        self._parent = parent
        self._g = parent.g + self.w

    def is_better_parent(self, parent: NodeG) -> bool:
        """
        ========================================================================
         Returns True if the received Parent is better than the current
                  (lower G-Value).
        ========================================================================
        """
        return self.g > parent.g + self.w

    def __lt__(self, other: NodeG) -> bool:
        return self.g > other.g

    def __le__(self, other: NodeG) -> bool:
        return self._g >= other.g

    def __gt__(self, other: NodeG) -> bool:
        return self.g < other.g

    def __ge__(self, other: NodeG) -> bool:
        return self._g <= other.g

    @classmethod
    def from_node_cell(cls, node: NodeCell) -> NodeG:
        """
        ========================================================================
         Converts NodeCell into NodeG.
        ========================================================================
        """
        return cls(cell=node.cell, name=node.name, parent=node.parent)
