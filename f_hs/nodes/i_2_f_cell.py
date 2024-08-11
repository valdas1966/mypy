from __future__ import annotations
from f_hs.nodes.i_1_f import NodeF
from f_graph.nodes.i_1_path_cell import NodePathCell, Cell


class NodeFCell(NodeF, NodePathCell):
    """
    ============================================================================
     Informed NodeF represents list Cell in the Grid.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell = Cell(),
                 name: str = None,
                 parent: NodeFCell = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeF.__init__(self, name=name, parent=parent)
        NodePathCell.__init__(self, name=name, cell=cell)

    def __repr__(self) -> str:
        """
        ========================================================================
         Ex: '<NodeFCell: A(0,0)> G=0, H=5, F=5'
        ========================================================================
        """
        return f'{NodePathCell.__repr__(self)} G={self.g}, H={self.h}, F={self.f()}'
