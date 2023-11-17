from f_data_structure.nodes.i_1_path import NodePath
from f_data_structure.f_grid.cell import Cell


class NodeCell(NodePath):
    """
    ============================================================================
     Node represents a Cell.
    ============================================================================
    """

    def __init__(self, cell: Cell) -> None:
        NodePath.__init__(self, name=cell.name)
        self._cell = cell

    def key_comparison(self) -> list:
        return self._cell.key_comparison()
