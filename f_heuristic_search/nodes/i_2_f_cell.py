from __future__ import annotations
from f_heuristic_search.nodes.i_2_f import NodeF
from f_data_structure.f_grid.cell import Cell


class NodeFCell(NodeF, Cell):
    """
    ============================================================================
     NodeF represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodeFCell = None) -> None:
        NodeF.__init__(self, name, parent)
        Cell.__init__(self, cell.row, cell.col)

    def __str__(self) -> str:
        return f'{self.name if self.name else str()}({self.row},{self.col})' \
               f'[g={self.g}, h={self.h}, f={self.f()}]'

    def __eq__(self, other: NodeFCell) -> bool:
        return Cell.__eq__(self, other)

    def __ne__(self, other: NodeFCell) -> bool:
        return Cell.__ne__(self, other)
