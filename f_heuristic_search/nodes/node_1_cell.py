from __future__ import annotations
from f_heuristic_search.nodes.node_0_base import NodeBase
from f_data_structure.f_grid.cell import Cell


class NodeCell(NodeBase, Cell):
    """
    ============================================================================
     Node that represents a Cell in a 2D-Grid.
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
        4. comparison funcs based on row-major system.
    ============================================================================
    """

    _name: str                        # Node's Name
    _parent: NodeCell                 # Node's Parent
    _children: list[NodeCell]         # Node's Children
    _row: int                         # Node's Row
    _col: int                         # Node's Col

    def __init__(self,
                 row: int = 0,
                 col: int = None,
                 name: str = None,
                 parent: NodeCell = None,
                 cell: Cell = None) -> None:
        if cell:
            row, col = cell.row, cell.col
        NodeBase.__init__(self, name=name, parent=parent)
        Cell.__init__(self, row=row, col=col)

    def __str__(self) -> str:
        """
        ========================================================================
         Returns str in format of 'name(row,col)'
        ========================================================================
        """
        str_node_base = NodeBase.__str__(self)
        str_cell = Cell.__str__(self)
        return f'{str_node_base}{str_cell}'
