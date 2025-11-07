from __future__ import annotations
from f_graph.nodes.i_1_parent import NodeParent
from f_ds.old_grids.old_grid import Cell
from typing import Iterable


class NodeCell(NodeParent[Cell]):
    """
    ========================================================================
     A Node that contains a Cell.
    ========================================================================
    """

    def __init__(self,
                 key: Cell,
                 parent: Cell = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Node.
        ========================================================================
        """
        NodeParent.__init__(self, key=key, parent=parent, name=name)
        self._cell = key

    def distance(self, other: NodeCell) -> int:
        """
        ========================================================================
         Return the distance between the two Nodes based on their Cells.
        ========================================================================
        """
        return self.cell.distance(other.cell)

    def farthest(self, nodes: Iterable[NodeCell]) -> NodeCell:
        """
        ========================================================================
         Return the farthest Node from the current Node based on their Cells.
        ========================================================================
        """
        cells = [other.cell for other in nodes]
        cells_farthest = self.cell.farthest(cells=cells)
        for node in nodes:
            if node.cell == cells_farthest:
                return node

    @property
    def cell(self) -> Cell:
        """
        ========================================================================
         Get the Node's Cell.
        ========================================================================
        """
        return self._cell

    def __str__(self) -> str:
        """
        ========================================================================
         Return a string representation of the Node.
        ========================================================================
        """
        return str(self.cell)
