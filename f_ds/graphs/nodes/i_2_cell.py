from __future__ import annotations
from f_ds.graphs.nodes.i_1_path import NodePath
from f_ds.grids.cell import Cell
from f_utils import u_str


class NodeCell(Cell):
    """
    ============================================================================
     Node represents a Cell in the Grid.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell(),
                 parent: NodeCell = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodePath.__init__(self, name=name, parent=parent)
        self._cell = cell

    @property
    def cell(self) -> Cell:
        return self._cell

    # Override NodeBase
    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by (Row, Col) and not by Name.
        ========================================================================
        """
        return self._cell.key_comparison()

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR.
         Ex: 'Name(1,2)'
        ========================================================================
        """
        prefix = NodePath.__str__(self)
        text = str(self._cell)
        return u_str.add_prefix(prefix=prefix, text=text)

    def __hash__(self) -> int:
        """
        ========================================================================
         Return NodeCell Hash-Value.
        ========================================================================
        """
        return hash(self._cell)
