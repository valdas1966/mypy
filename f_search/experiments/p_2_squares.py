from f_log.utils import set_debug, log_1, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.algos.i_1_spp.utils import are_reachable, cells_reachable, ne
from f_utils import u_pickle, u_iter
import random

PairCells = tuple[Cell, Cell]
Square = list[Cell]
PairSquares = tuple[Square, Square]
DictSquares = dict[str, list[PairSquares]]


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_1
def get_pair_cells(grid: Grid, distance_min: int) -> PairCells:
    """
    ========================================================================
     1. Get a pair of cells from the grid.
     2. The distance between the cells >= distance_min.
     3. The cells are reachable to each other.
    ========================================================================
    """
    p_1 = lambda a, b: a.distance(other=b) >= distance_min
    p_2 = lambda a, b: are_reachable(grid, a, b)
    predicate = lambda a, b: p_1(a, b) and p_2(a, b)
    pair = u_iter.pairs(items=grid.cells_valid(),
                         size=1,
                         predicate=predicate)[0]
    return pair

@log_2
def get_pair_squares(grid: Grid,
                     distance_min: int,
                     steps_max: int,
                     size_min: int) -> PairSquares:
    """
    ========================================================================
     1. Get a pair of squares from the grid.
     2. The squares have at least size_min cells.
    ========================================================================
    """
    while True:
        pair_cells = get_pair_cells(grid=grid, distance_min=distance_min)
        cell_a, cell_b = pair_cells
        square_a = cells_reachable(grid, cell_a, steps_max)
        if len(square_a) < size_min:
            continue
        random.shuffle(square_a)
        square_b = cells_reachable(grid, cell_b, steps_max)
        if len(square_b) < size_min:
            continue
        random.shuffle(square_b)
        return (square_a, square_b)

@log_2
def get_squares(grid: Grid,
                distance_min: int,
                steps_max: int,
                size_min: int,
                n: int) -> list[PairSquares]:
    """
    ========================================================================
     Get n-pairs of squares from the grid.
    ========================================================================
    """
    func = lambda: get_pair_squares(grid, distance_min, steps_max, size_min)
    return [func() for _ in range(n)]
    
@log_2
def squares_from_grids(grids: dict[str, Grid],
                       distance_min: int,
                       steps_max: int,
                       size_min: int,
                       n: int) -> DictSquares:
    """
    ========================================================================
     Get n-pairs of squares from the grids.
    ========================================================================
    """
    d: dict[str, list[PairSquares]] = dict()
    for grid in grids.values():
        squares = get_squares(grid, distance_min, steps_max, size_min, n)
        d[grid.name] = squares
    return d

@log_2
def squares_to_pickle(squares: DictSquares, pickle_squares: str) -> None:
    """
    ========================================================================
     Pickle the DictSquares to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=squares, path=pickle_squares)

        
"""
===============================================================================
 Main - Generate Random-Pairs for a List of Grids.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid].
 Output: Pickle of dict[Grid.Name -> List[PairSquares]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_squares = 'f:\\paper\\i_2_squares\\squares.pkl'

# Number of Pairs to Generate for each Grid.
n = 1
# Minimum Distance between the Pairs.
distance_min = 100
# Radius of the Diamond
steps_max = 5
# Minimum size of Cells in the Diamond
size_min = 50


@log_2
def main(pickle_grids: str,
         pickle_squares: str,
         distance_min: int,
         steps_max: int,
         size_min: int,
         n: int) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """    
    grids = load_grids(pickle_grids)
    squares = squares_from_grids(grids,
                                 distance_min,
                                 steps_max,
                                 size_min,
                                 n)
    squares_to_pickle(squares, pickle_squares)


main(pickle_grids, pickle_squares, distance_min, steps_max, size_min, n)
