from __future__ import annotations
from f_ds.grids.grid import Grid
from f_ds.graphs.i_0_base import GraphBase
from f_ds.graphs.nodes.i_1_cell import NodeCell
from typing import Type


class GraphGrid(GraphBase):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 name: str = None,
                 type_node: Type[NodeCell] = NodeCell) -> None:
        """
        ========================================================================
         1. Init private Attributes.
         2. The Object can be initialized by [Rows & Cols | Grid].
         3. If only the Rows are provided, the Grid will be square.
        ========================================================================
        """
        GraphBase.__init__(self, name=name)
        self._grid = grid
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

    @property
    def type_node(self) -> Type[NodeCell]:
        return self._type_node

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

    def get_neighbors(self, node: NodeCell) -> list[NodeCell]:
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

    def __getitem__(self, index: int) -> list[NodeCell]:
        """
        ========================================================================
         1. Direct access to a Row of Nodes by [Row] Property.
         2. Direct access to a specific Node by [Row][Col] Properties.
        ========================================================================
        """
        return self._nodes[index]

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the GraphGrid (Boolean-Grid based on Cell-Validity).
        ========================================================================
        """
        return str(self._grid)

    @classmethod
    def from_grid(cls,
                  grid: GridCells,
                  name: str = None,
                  type_node: Type[NodeCell] = NodeCell) -> GraphGrid:
        """
        ========================================================================
         Create GraphGrid by a given GridCells.
        ========================================================================
        """
        return cls(grid=grid, name=name, type_node=type_node)

    @classmethod
    def from_shape(cls,
                   rows: int,
                   cols: int = None,
                   name: str = None,
                   type_node: Type[NodeCell] = NodeCell) -> GraphGrid:
        """
        ========================================================================
         Create GraphGrid by a given Shape (Rows and Cols).
        ========================================================================
        """
        grid = GridCells(rows=rows, cols=cols)
        return cls.from_grid(grid=grid, name=name, type_node=type_node)

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_non_valid: int = 0,
                 type_node: Type[NodeCell] = NodeCell) -> GraphGrid:
        """
        ========================================================================
         Generates a Graph with a random Grid based on received params
             (size and percentage of invalid cells).
        ========================================================================
        """
        grid = GridCells.generate(rows=rows,
                                  cols=cols,
                                  pct_non_valid=pct_non_valid)
        return cls.from_grid(grid=grid, type_node=type_node)

    @classmethod
    def generate_list(cls,
                      cnt: int,
                      rows: int,
                      cols: int = None,
                      pct_non_valid: int = 0,
                      type_node: Type[NodeCell] = NodeCell
                      ) -> list[GraphGrid]:
        """
        ========================================================================
         Generates a List of Graphs with a random Grid based on received
          params (size and percentage of invalid cells).
        ========================================================================
        """
        return [cls.generate(rows, cols, pct_non_valid, type_node)
                for _ in range(cnt)]
