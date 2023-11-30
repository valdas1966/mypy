from f_data_structure.nodes.i_0_base import NodeBase
from f_data_structure.f_grid.cell import Cell


class NodeCell(NodeBase):
    """
    ============================================================================
     Node represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell()) -> None:
        NodeBase.__init__(self, name=name)
        self._cell = cell

    # Override NodePath
    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by (Row, Col) and not by Name.
        ========================================================================
        """
        return self._cell.key_comparison()

    def __str__(self) -> str:
        return (self._name or str()) + self._cell.__str__()
