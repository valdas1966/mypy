from __future__ import annotations
from f_data_structure.graphs.i_0_base import GraphBase
from f_data_structure.f_grid.grid_cells import GridCells
from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class GraphGrid(Generic[Node], GraphBase):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 grid: GridCells = None) -> None:
        """
        ========================================================================
         1. Init private Attributes.
         2. The Object can be initialized by Rows & Cols or by a Grid.
        ========================================================================
        """
        GraphBase.__init__(self, name=name)
        if not grid:
            cols = cols or rows
            grid = GridCells(rows, cols)
        self._grid = grid
        self._nodes = [
                        [Node(cell=self._grid[row][col])
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

    def get_neighbors(self, node: Node) -> list[Node]:
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
         Turn the received Tuples (Coordinates) to Invalid.
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
        return GraphGrid[type_node](grid=grid)
