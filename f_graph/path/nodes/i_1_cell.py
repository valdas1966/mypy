from __future__ import annotations
from f_graph.path.nodes.i_0_path import NodePath
from f_ds.grids.cell import Cell


class NodeCell(NodePath[Cell]):
    """
    ============================================================================
     NodePath with Cell property.
    ============================================================================
    """

    def __init__(self,
                 uid: Cell = Cell(),
                 name: str = None,
                 parent: NodeCell = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodePath.__init__(self, uid=uid, name=name, parent=parent)
