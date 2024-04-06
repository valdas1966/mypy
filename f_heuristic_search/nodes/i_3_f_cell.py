from __future__ import annotations
from f_heuristic_search.nodes.i_2_f import NodeF
from f_data_structure.nodes.i_2_cell import NodeCell
from f_data_structure.f_grid.cell import Cell


class NodeFCell(NodeF, NodeCell):
    """
    ============================================================================
     NodeF represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell()) -> None:
        NodeF.__init__(self, name=name)
        NodeCell.__init__(self, name=name, cell=cell)

    def __str__(self) -> str:
        return f'{NodeCell.__str__(self)}' \
               f'[g={self.g}, h={self.h}, f={self.f()}]'

    def key_comparison(self) -> list:
        return [NodeF.key_comparison(self), NodeCell.key_comparison(self)]
