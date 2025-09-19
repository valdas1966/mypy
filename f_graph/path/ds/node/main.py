from f_ds.nodes import NodeParent
from f_ds.grids import Cell
from typing import Self


class NodeQuick(NodeParent[Cell]):
    """
    ============================================================================
     NodeCell with a Parent.
    ============================================================================
    """

    def __init__(self,
                 cell: Cell,
                 h: int = None,
                 name: str = 'NodeQuick',
                 parent: Self = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeParent.__init__(self, key=cell, name=name, parent=parent)
        self._g = 0 if not parent else parent.g + 1
        self._h = h
        self.is_cached = False
        self.is_bounded = False

    @property
    def cell(self) -> Cell:
        """
        ========================================================================
         Get the cell.
        ========================================================================
        """
        return self.key
    
    @property
    def g(self) -> int:
        """
        ========================================================================
         Get the g-value.
        ========================================================================
        """
        return self._g

    @property
    def h(self) -> int:
        """
        ========================================================================
         Get the h-value.
        ========================================================================
        """
        return self._h
    
    