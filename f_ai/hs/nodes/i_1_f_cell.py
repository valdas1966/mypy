from __future__ import annotations
from f_ai.hs.nodes.i_1_f import NodeF
from f_graph.path.nodes.i_1_cell import NodeCell, Cell


class NodeFCell(NodeF, NodeCell):
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
        NodeCell.__init__(self, name=name, cell=cell)

    def __eq__(self, other: NodeFCell) -> bool:
        """
        ========================================================================
         Set Equality by Cell and not by Node (because Node.h can be None).
        ========================================================================
        """
        return self.uid == other.uid

    def __nq__(self, other: NodeFCell) -> bool:
        """
        ========================================================================
         Set Equality by Cell and not by Node (because Node.h can be None).
        ========================================================================
        """
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """
        ========================================================================
         Ex: '<NodeFCell: A(0,0)> G=0, H=5, F=5'
        ========================================================================
        """
        return f'{NodeCell.__repr__(self)} G={self.g}, H={self.h}, F={self.f()}'
