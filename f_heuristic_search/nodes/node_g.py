from f_data_structure.cell import Cell


class NodeG(Cell):
    """
    ============================================================================
     Desc: Represents a Node with a Weight-Value (w) and a
            Cost-Value-From-The-Start (g).
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. w (int)                 : Weight from the parent to this node.
        2. g (int)                 : Cost from the start node to this node.
        3. parent (NodeG)          : The predecessor node in the path.
                                     (g) updates automatically on parent update.
    ============================================================================
    """

    def __init__(self,
                 x: int = None,           # Node's X-Coordinate in the Grid.
                 y: int = None,           # Node's Y-Coordinate in the Grid.
                 name: str = None,        # Node's Name.
                 cell: Cell = None,       # Node's Position in the Grid
                 parent: 'NodeG' = None   # Parent-Node in the Grid.
                                          #  None if this is a Start-Node.
                 ) -> None:
        """
        ========================================================================
         Desc: Generate a new NodeG object.
                Computes G-Value based on Cost from the Start to the
                 Parent-Node + current Node's Weight.
        ========================================================================
        """
        if cell:
            x, y, name = cell.x, cell.y, cell.name
        super().__init__(x, y, name)
        self._w = 1
        self._parent = parent
        self._g = parent.g + self._w if parent else 0

    @property
    def w(self) -> int:
        return self._w

    @property
    def g(self) -> int:
        return self._g

    @property
    def parent(self) -> 'NodeG':
        return self._parent

    @parent.setter
    def parent(self, parent_new) -> None:
        self._parent = parent_new
        self._g = parent_new.g + self._w
