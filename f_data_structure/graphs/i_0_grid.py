from f_data_structure.graphs.abc.base import GraphBase
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.nodes.i_2_cell import NodeCell as Node
from typing import Type


class GraphGrid(GraphBase):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 rows: int = None,
                 cols: int = None,
                 name: str = None,
                 grid: Grid = None,
                 type_node: Type[Node] = Node) -> None:
        if grid and not name:
            name = grid.name
        GraphBase.__init__(self, name=name)
        if rows:
            cols = cols or rows
            grid = Grid(rows, cols)
        self._grid = grid
        self._type_node = type_node
        self._nodes = [
                        [type_node(cell=grid[row][col])
                         for col
                         in range(grid.cols)]
                        for row in range(grid.rows)
                      ]

    def get_neighbors(self, node: Node) -> list[Type[Node]]:
        """
        ========================================================================
         Return list of a given Node's neighbors.
        ========================================================================
        """
        return [self._nodes[cell.row][cell.col]
                for cell
                in self._grid.neighbors(node.cell)]

    def make_invalid(self, tuples: list[tuple]) -> None:
        """
        ========================================================================
         Turn the received Tuples to Invalid.
        ========================================================================
        """
        self._grid.make_invalid_tuples(tuples)

    def __getitem__(self, index: int) -> list[Node]:
        """
        ========================================================================
         1. Direct access to a Row of Nodes by [Row] Property.
         2. Direct access to a specific Node by [Row][Col] Properties.
        ========================================================================
        """
        return self._nodes[index]
