from __future__ import annotations
from f_graph.nodes.i_2_g import NodeG
from f_graph.nodes.mixins.has_cell import HasCell, Cell


class NodeGCell(NodeG, HasCell):
    """
    ============================================================================
     Node-G with Cell.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 name: str = None,
                 parent: NodeGCell = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeG.__init__(self, name=name, parent=parent)
        HasCell.__init__(self, cell=cell)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by G (reverse) and by Cell.
        ========================================================================
        """
        return [-self.g, self.cell.key_comparison()]

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: Node(1,2).
        ========================================================================
        """
        return f'{NodeG.__str__(self)}({str(self.cell)})'

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Cell.
        ========================================================================
        """
        return hash(self.cell)
