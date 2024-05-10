from __future__ import annotations
from f_hs.nodes.i_2_f import NodeF
from f_ds.nodes.i_2_cell import NodeCell
from f_ds.cell import Cell


class NodeFCell(NodeF, NodeCell):
    """
    ============================================================================
     NodeF represents a Cell.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeFCell = None,
                 cell: Cell = Cell()) -> None:
        NodeF.__init__(self, name=name, parent=parent)
        NodeCell.__init__(self, name=name, parent=parent, cell=cell)

    def __str__(self) -> str:
        return f'{NodeCell.__str__(self)}'

    def __repr__(self) -> str:
        return (f'<NodeFCell: name={self.name}, cell={self.cell}, g={self.g}, '
                f'h={self.h}, f={self.f()}]')

    def key_comparison(self) -> list:
        return [NodeF.key_comparison(self), NodeCell.key_comparison(self)]
