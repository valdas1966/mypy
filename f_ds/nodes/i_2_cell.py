from f_ds.nodes.i_1_parent import NodeParent
from f_ds.grids.grid import Cell


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
