from __future__ import annotations
from f_heuristic_search.nodes.node_1_cell import NodeCell
from f_heuristic_search.alias.cell import Cell


class NodeH(NodeCell):
    """
    ============================================================================
     Node with a H-Value (Heuristic Value to the Goal-Node).
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. name (str)               : Node's Name.
        2. row (int)                : Node's Row.
        3. col (int)                : Node's Col.
        4. parent (NodeH)           : Node's Parent.
        5. children (list[NodeH])   : Node's Children.
        6. h (int)                  : Heuristic Cost to Goal.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodeH = None,
                 h: int = None) -> None:
        NodeCell.__init__(self, cell=cell, name=name, parent=parent)
        self._h = h

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, h_new: int) -> None:
        self._h = h_new
