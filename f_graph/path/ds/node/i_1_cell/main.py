from f_ds.nodes import NodeParent
from f_ds.grids import Cell
from typing import Self


class NodeCell(NodeParent[Cell]):
    """
    ============================================================================
     NodeCell with a Parent.
    ============================================================================
    """

    # Factory
    Factory: type = None
    
    def __init__(self,
                 cell: Cell,
                 name: str = 'NodeCell',
                 parent: Self = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeParent.__init__(self, key=cell, name=name, parent=parent)

    @property
    def cell(self) -> Cell:
        """
        ========================================================================
         Get the cell.
        ========================================================================
        """
        return self.key
    