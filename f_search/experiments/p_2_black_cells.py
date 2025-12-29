from f_log.utils import set_debug, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the Grids from the Pickle File.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_2
def get_black_cells(grids: dict[str, Grid],
                    distance: int,
                    min_valid_neighbors: int) -> dict[str, set[Cell]]:
    """
    ============================================================================
     Find the Black Cells in the Grids.
    ============================================================================
    """
    @log_2
    def for_grid(grid: Grid) -> set[Cell]:
        """
        ========================================================================
         Find the Black Cells in the Grid.
        ========================================================================
        """
        black_cells: set[Cell] = set()
        for cell in grid:
            rect = grid.select.rect_around(cell=cell, distance=distance)
            if len(list(rect)) < min_valid_neighbors:
                black_cells.add(cell)
        return black_cells
    return {name: for_grid(grid) for name, grid in grids.items()}


@log_2
def pickle_results(results: dict[str, set[Cell]], pickle_results: str) -> None:
    """
    ============================================================================
     Pickle the Results to the Pickle File.
    ============================================================================
    """
    u_pickle.dump(obj=results, path=pickle_results)


"""
===============================================================================
 Main - Find the Black Cells (not enough valid neighbors) for each Grid.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid].
 Output: Pickle of dict[Grid.Name -> set[Cell]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_black_cells = 'f:\\paper\\i_2_black_cells\\black_cells.pkl'
min_valid_neighbors = 50
distance = 5

@log_2
def main(pickle_grids: str,
         pickle_black_cells: str,
         min_valid_neighbors: int,
         distance: int) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """
    grids = load_grids(pickle_grids)
    black_cells = get_black_cells(grids, distance, min_valid_neighbors)
    pickle_results(black_cells, pickle_black_cells)


main(pickle_grids, pickle_black_cells, min_valid_neighbors, distance)
