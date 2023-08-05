from f_data_structure.old_cell import Cell


class NodeH(Cell):

    def __init__(self,
                 x: int = None,  # Node's X-Coordinate in the Grid.
                 y: int = None,  # Node's Y-Coordinate in the Grid.
                 name: str = None,  # Node's Name.
                 cell: Cell = None,  # Node's Position in the Grid
                 ) -> None:
        if cell:
            x, y, name = cell.x, cell.y, cell.name
        super().__init__(x, y, name)
        self._h = None

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, value: int) -> None:
        self._h = value
