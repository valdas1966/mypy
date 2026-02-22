from f_log.old.utils import set_debug, log_1, log_2
from f_search.ds.state import StateCell as State
from f_search.algos.i_1_neighborhood import BFSNeighborhood
from f_search.problems import ProblemNeighborhood
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.algos.i_1_spp.utils import are_reachable
from f_utils import u_pickle, u_iter
import random

PairCells = tuple[Cell, Cell]
Diamond = list[State]
PairDiamonds = tuple[Diamond, Diamond]
DictDiamonds = dict[str, list[PairDiamonds]]


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
def get_pair_diamonds(grid: Grid,
                      distance_min: int,
                      steps_max: int,
                      size_min: int) -> PairDiamonds:
    """
    ========================================================================
     1. Get a pair of diamonds from the grid.
     2. The diamonds have at least size_min cells.
    ========================================================================
    """
    while True:
        pair_cells = get_pair_cells(grid=grid, distance_min=distance_min)
        cell_a, cell_b = pair_cells
        state_a, state_b = State(key=cell_a), State(key=cell_b)
        problem_a = ProblemNeighborhood(grid=grid, start=state_a, steps_max=steps_max)
        bfs_a = BFSNeighborhood(problem=problem_a)
        diamond_a = list(bfs_a.run().neighborhood)
        if len(diamond_a) < size_min:
            continue
        random.shuffle(diamond_a)
        problem_b = ProblemNeighborhood(grid=grid, start=state_b, steps_max=steps_max)
        bfs_b = BFSNeighborhood(problem=problem_b)
        diamond_b = list(bfs_b.run().neighborhood)
        if len(diamond_b) < size_min:
            continue
        random.shuffle(diamond_b)
        return diamond_a, diamond_b

@log_2
def get_diamonds(grid: Grid,
                 distance_min: int,
                 steps_max: int,
                 size_min: int,
                 n: int) -> list[PairDiamonds]:
    """
    ========================================================================
     Get n-pairs of diamonds from the grid.
    ========================================================================
    """
    func = lambda: get_pair_diamonds(grid, distance_min, steps_max, size_min)
    return [func() for _ in range(n)]
    
@log_2
def diamonds_from_grids(grids: dict[str, Grid],
                        distance_min: int,
                        steps_max: int,
                        size_min: int,
                        n: int) -> DictDiamonds:
    """
    ========================================================================
     Get n-pairs of diamonds from the grids.
    ========================================================================
    """
    d: dict[str, list[PairDiamonds]] = dict()
    for grid in grids.values():
        diamonds = get_diamonds(grid, distance_min, steps_max, size_min, n)
        d[grid.name] = diamonds
    return d

@log_2
def diamonds_to_pickle(diamonds: DictDiamonds, pickle_diamonds: str) -> None:
    """
    ========================================================================
     Pickle the DictDiamonds to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=diamonds, path=pickle_diamonds)

        
"""
===============================================================================
 Main - Generate Random-Pairs for a List of Grids.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid].
 Output: Pickle of dict[Grid.Name -> List[PairDiamonds]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_diamonds = 'f:\\paper\\i_2_diamonds\\diamonds.pkl'

# Number of Pairs to Generate for each Grid.
n = 10
# Minimum Distance between the Pairs.
distance_min = 100
# Radius of the Diamond
steps_max = 15
# Minimum size of Cells in the Diamond
size_min = 100


@log_2
def main(pickle_grids: str,
         pickle_diamonds: str,
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
    diamonds = diamonds_from_grids(grids,
                                   distance_min,
                                   steps_max,
                                   size_min,
                                   n)
    diamonds_to_pickle(diamonds, pickle_diamonds)


main(pickle_grids, pickle_diamonds, distance_min, steps_max, size_min, n)
