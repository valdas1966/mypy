from f_data_structure.old_cell import Cell


class NodeG(Cell):

    def __init__(self, cell: Cell) -> None:
        super().__init__(x=cell.x, y=cell.y, name=cell.name)
