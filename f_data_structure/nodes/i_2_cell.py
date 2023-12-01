from __future__ import annotations
from f_data_structure.nodes.i_1_path import NodePath
from f_data_structure.f_grid.cell import Cell


class NodeCell(NodePath):
    """
    ============================================================================
     Node represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell(),
                 parent: Cell = None) -> None:
        NodePath.__init__(self, name=name, parent=parent)
        self._cell = cell

    @property
    def cell(self) -> Cell:
        return self._cell

    # Override NodePath
    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by (Row, Col) and not by Name.
        ========================================================================
        """
        return self._cell.key_comparison()

    def distance(self, other: NodeCell) -> int:
        """
        ========================================================================
         Return the Distance between the Nodes' Cells.
        ========================================================================
        """
        return self.cell.distance(other.cell)

    def __str__(self) -> str:
        return (self._name or str()) + self._cell.__str__()

    def __hash__(self) -> int:
        return self._cell.__hash__()
