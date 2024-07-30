from __future__ import annotations
from f_graph.nodes.i_1_path import NodePath
from f_graph.nodes.mixins.has_cell import HasCell, Cell


class NodePathCell(NodePath, HasCell):
    """
    ============================================================================
     NodePath with Cell property.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodePathCell = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodePath.__init__(self, name=name, parent=parent)
        HasCell.__init__(self, cell=cell)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by Cell.
        ========================================================================
        """
        return self.cell.key_comparison()

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: A(1,2)
        ========================================================================
        """
        return f'{NodePath.__str__(self)}{str(self.cell)}'

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Cell.
        ========================================================================
        """
        return hash(self.cell)
