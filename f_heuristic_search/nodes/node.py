from f_data_structure.cell import Cell


class Node(Cell):
    """
    ============================================================================
     Desc: Represents a Node in the Grid.
    ============================================================================
     Inherited Members:
    ----------------------------------------------------------------------------
        1. name (str)            : Node's Name.
        2. x (int)               : Node's X-Coordinate.
        3. y (int)               : Node's Y-Coordinate.

    """

    def __init__(self,
                 x: int = None,         # Node's X-Coordinate in the Grid.
                 y: int = None,         # Node's Y-Coordinate in the Grid.
                 name: str = None,      # Node's Name.
                 cell: Cell = None,     # Node's Position in the Grid
                 parent: 'Node' = None  # Parent-Node in the Grid.
                                        #  None if this is a Start-Node.
                 ) -> None:
        """
        ========================================================================
         Desc: Init the Node object with Node's Parent and Weight value.
        ========================================================================
        """
        if cell:
            x, y, name = cell.x, cell.y, cell.name
        super().__init__(x, y, name)
        self._w = 1
        self._parent = parent

    @property
    def w(self) -> int:
        return self._w

    @property
    def parent(self) -> 'Node':
        return self._parent

    @parent.setter
    def parent(self, parent_new: 'Node') -> None:
        self._parent = parent_new
