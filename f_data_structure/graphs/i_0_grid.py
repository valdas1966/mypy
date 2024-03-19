from __future__ import annotations
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
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 type_node: Type[Node] = Node) -> None:
        GraphBase.__init__(self, name=name)
        cols = cols or rows
        self._grid = Grid(rows, cols)
        self._type_node = type_node
        self._nodes = [
                        [type_node(cell=self._grid[row][col])
                         for col
                         in range(self._grid.cols)]
                        for row in range(self._grid.rows)
                      ]

    @property
    def rows(self) -> int:
        return self._grid.rows

    @property
    def cols(self) -> int:
        return self._grid.cols

    def shape(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Grid's Shape (dimensions).
        ========================================================================
        """
        return self._grid.shape()

    def pct_non_valid(self) -> int:
        """
        ========================================================================
         Return the Percentage of the Non-Valid Cells in the Grid.
        ========================================================================
        """
        return self._grid.pct_non_valid()

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

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_non_valid: int = 0,
                 type_node: Type[Node] = Node) -> GraphGrid:
        """
        ========================================================================
         Generates a Graph with a random Grid based on received params
          (size and percentage of invalid cells).
        ========================================================================
        """
        grid = Grid.generate(rows=rows, cols=cols, pct_non_valid=pct_non_valid)
        return GraphGrid(grid=grid, type_node=type_node)
