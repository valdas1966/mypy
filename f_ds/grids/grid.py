from f_ds.collections.i_2d import Collection2D
from f_ds.grids.cell import Cell


class Grid(Collection2D[Cell]):

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        Collection2D.__init__(self, name=name, rows=rows, cols=cols)
        self._items = [
                        [Cell(row, col)
                         for col in range(self.cols)]
                        for row in range(self.rows)
                        ]

