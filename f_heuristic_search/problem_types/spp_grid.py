from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.nodes.i_2_f_cell import NodeFCell as Node
from f_data_structure.f_grid.cell import Cell
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.graphs.i_1_grid import GraphGrid as Graph


class SPPGrid(SPP):
    """
    ============================================================================
     Represents a Shortest-Path-Problem Type in 2D-Grids.
    ============================================================================
    """

    def __init__(self,
                 start: Cell,
                 goal: Cell,
                 grid: Grid) -> None:
        graph = Graph(grid=grid)
        start = graph.cell_to_node(cell=start)
        goal = graph.cell_to_node(cell=goal)
        SPP.__init__(self, start, goal, graph)
        self._grid = grid

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_valid: int = 0
                 ) -> SPP:
        """
        ========================================================================
         Generates a random SPP based on the given arguments, which include the
          grid size, as well as random locations for the start, goal, and
          invalid nodes.
        ========================================================================
        """
        grid = Grid.generate(rows=rows,
                             cols=cols,
                             name=name,
                             pct_non_valid=pct_non_valid)
        # Ensure the Grid can accommodate both Start and Goal Cells
        if len(grid.cells()) < 2:
            return None
        start, goal = grid.cells_random(size=2)
        return SPPGrid(grid, start, goal)
