from f_data_structure.cell import Cell


class Node(Cell):

    def __init__(self
                 x: int = None,         # Node's X-Coordinate in the Grid.
                 y: int = None,         # Node's Y-Coordinate in the Grid.
                 name: str = None,      # Node's Name.
                 cell: Cell = None,     # Node's Position in the Grid
                 parent: 'Node' = None  # Parent-Node in the Grid.
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