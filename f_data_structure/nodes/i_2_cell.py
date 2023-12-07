from __future__ import annotations
from f_data_structure.nodes.i_1_path import NodePath
from f_data_structure.f_grid.cell import Cell
from f_utils import u_str


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
        return self._cell.distance(other.cell)

    def to_tuple(self) -> tuple[int, int]:
        """
        ========================================================================
         Return Cell's Coordinates.
        ========================================================================
        """
        return self._cell.to_tuple()

    def __str__(self) -> str:
        text = str(self._cell)
        prefix = self._name
        return u_str.add_prefix(text, prefix)

    def __hash__(self) -> int:
        return self._cell.__hash__()
