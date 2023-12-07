from __future__ import annotations
from f_heuristic_search.nodes.i_2_f import NodeF
from f_data_structure.nodes.i_2_cell import NodeCell
from f_data_structure.f_grid.cell import Cell


class Node(NodeF, NodeCell):
    """
    ============================================================================
     NodeF represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell(),
                 parent: Node = None) -> None:
        NodeF.__init__(self, name=name, parent=parent)
        NodeCell.__init__(self, name=name, parent=parent, cell=cell)

    def __str__(self) -> str:
        return f'{NodeCell.__str__(self)}' \
               f'[g={self.g}, h={self.h}, f={self.f()}]'
