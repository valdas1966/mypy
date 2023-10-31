from __future__ import annotations
from f_data_structure.nodes.node_2_cell import NodeCell


class NodeH(NodeCell):
    """
    ============================================================================
     Node with a H-Value (Heuristic cost for reaching the Goal).
    ============================================================================
      Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: NodeCell) -> int
           [*] Manhattan-Distance between the Nodes.
        2. path_from(other: NodeBase) -> list[NodeBase]
          [*] Returns a Path from a given Node to the Current.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. comparison funcs based on row-major system.
    ============================================================================
    """

    _name: str                  # Node's Name
    _parent: NodeH              # Node's Parent
    _children: list[NodeH]      # Node's Children
    _row: int                   # Node's Row
    _col: int                   # Node's Col
    _h: int                     # Heuristic-Cost for reaching the Goal

    def __init__(self,
                 row: int = 0,
                 col: int = None,
                 name: str = None,
                 parent: NodeH = None,
                 h: int = None
                 ) -> None:
        NodeCell.__init__(self, row=row, col=col, name=name, parent=parent)
        self._h = h

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, h_new: int) -> None:
        self._h = h_new
