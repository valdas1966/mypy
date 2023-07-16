from f_data_structure.interfaces.xyable import XYAble


class Grid:
    """
    ============================================================================
     Desc: Represents a general 2D grid of XYAble elements.
           Returns a XYAble element by index [x][y].
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. rows (int)              : Number of Grid's Rows.
        2. cols (int)              : Number of Grid's Columns.
        3. count_elements (int)    : Count of Grid's Elements.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. shape() -> str
        2. elements() -> list[XYAble]
        3. is_valid(x: int, y: int) -> bool
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 ele: XYAble = XYAble
                 ) -> None:
        cols = cols or rows
        self._rows = rows
        self._cols = cols if cols else rows
        self._grid = [[ele(x, y) for y in range(cols)] for x in range(rows)]

    def __getitem__(self, index) -> list[XYAble]:
        return self._grid[index]

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def count_elements(self) -> int:
        return len(self.elements())

    def shape(self) -> str:
        """
        ========================================================================
         Desc: Return a Grid's Shape in (rows,cols) string format.
        ========================================================================
        """
        return f'({self.rows},{self.cols})'

    def elements(self) -> list[XYAble]:
        """
        ========================================================================
         Desc: Return List of Grid's Elements.
        ========================================================================
        """
        return [e for row in self._grid for e in row if self.is_valid(xy=e)]

    def neighbors(self, xy: XYAble) -> list[XYAble]:
        """
        ========================================================================
         Desc: Returns List[XYAble] of adjacent valid neighbors in
                clockwise order.
        ========================================================================
        """
        return [n for n in xy.neighbors() if self.is_valid(xy=n)]

    def is_valid(self,
                 x: int = None,
                 y: int = None,
                 xy: XYAble = None) -> bool:
        """
        ========================================================================
         Desc: Check if the given (X,Y) Coordinates are valid in the Grid.
        ========================================================================
        """
        if not isinstance(x, int):
            x, y = xy.x, xy.y
        is_x_valid = 0 <= x < self.rows
        is_y_valid = 0 <= y < self.cols
        return is_x_valid and is_y_valid
