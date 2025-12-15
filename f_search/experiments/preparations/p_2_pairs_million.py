from f_log.utils import set_debug, log_1, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle, u_iter
from collections import defaultdict

set_debug(True)


@log_1
def load_grids(pickle_grids: str) -> dict[str, list[Grid]]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_1
def generate_pairs_for_grid(grid: Grid,
                            min_distance: int,
                            size: int) -> list[tuple[Cell, Cell]]:
    """
    ============================================================================
     Generate pairs for a grid.
    ============================================================================
    """
    predicate = lambda x, y: x.distance(other=y) >= min_distance
    return u_iter.pairs(data=grid, size=size, predicate=predicate)


@log_2
def generate_pairs_for_grids(grids: list[Grid],
                             min_distance: int,
                             size: int) -> dict[str, list[tuple[Cell, Cell]]]:
    """
    ============================================================================
     Generate pairs for a list of grids.
    ============================================================================
    """
    return {grid.name: generate_pairs_for_grid(grid=grid, min_distance=min_distance, size=size) for grid in grids}

