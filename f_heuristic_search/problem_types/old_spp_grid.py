from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.f_grid.grid_cells import GridCells as Grid


class SPPGrid(SPP):
    """
    ============================================================================
     Represents a Shortest-Path-Problem Type in 2D-Grids.
    ============================================================================
    """

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
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
                             pct_non_valid=pct_non_valid)
        # Ensure the Grid can accommodate both Start and Goal Cells
        if len(grid.cells()) < 2:
            return None
        start, goal = grid.cells_random(size=2)
        return SPPGrid(grid, start, goal)
