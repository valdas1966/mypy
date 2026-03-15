from f_log import setup_log, get_log
from f_search.ds.state import StateCell as State
from f_search.algos.i_1_neighborhood import BFSNeighborhood
from f_search.problems import ProblemNeighborhood
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.algos.i_1_spp.utils import are_reachable
from f_utils import u_pickle, u_iter
import logging
import random

setup_log(sink='console', level=logging.DEBUG)
log = get_log(__name__)

PairCells = tuple[Cell, Cell]
Diamond = list[State]
PairDiamonds = tuple[Diamond, Diamond]
DictDiamonds = dict[str, list[PairDiamonds]]


def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    log.debug(f'load_grids({pickle_grids})')
    grids = u_pickle.load(path=pickle_grids)
    log.debug(f'load_grids -> {len(grids)} grids')
    return grids


def get_pair_cells(grid: Grid, distance_min: int) -> PairCells:
    """
    ========================================================================
     1. Get a pair of cells from the grid.
     2. The distance between the cells >= distance_min.
     3. The cells are reachable to each other.
    ========================================================================
    """
    log.debug(f'get_pair_cells(grid={grid.name}, '
              f'distance_min={distance_min})')
    p_1 = lambda a, b: a.distance(other=b) >= distance_min
    p_2 = lambda a, b: are_reachable(grid, a, b)
    predicate = lambda a, b: p_1(a, b) and p_2(a, b)
    pair = u_iter.pairs(items=grid.cells_valid(),
                         size=1,
                         predicate=predicate)[0]
    log.debug(f'get_pair_cells -> {pair}')
    return pair


def get_pair_diamonds(grid: Grid,
                      distance_min: int,
                      steps_max_a: int,
                      size_min_a: int,
                      steps_max_b: int,
                      size_min_b: int,
                      found: list[int],
                      n: int) -> PairDiamonds:
    """
    ========================================================================
     1. Get a pair of diamonds from the grid.
     2. Each diamond has its own steps_max and size_min configuration.
    ========================================================================
    """
    log.debug(f'get_pair_diamonds(grid={grid.name}, '
              f'steps=({steps_max_a},{steps_max_b}), '
              f'size=({size_min_a},{size_min_b}))')
    attempt = 0
    while True:
        attempt += 1
        pair_cells = get_pair_cells(grid=grid,
                                    distance_min=distance_min)
        cell_a, cell_b = pair_cells
        state_a, state_b = State(key=cell_a), State(key=cell_b)
        # Diamond A
        problem_a = ProblemNeighborhood(grid=grid,
                                        start=state_a,
                                        steps_max=steps_max_a)
        bfs_a = BFSNeighborhood(problem=problem_a)
        diamond_a = list(bfs_a.run().neighborhood)
        if len(diamond_a) < size_min_a:
            log.debug(f'attempt {attempt}: '
                      f'\033[91mFAIL\033[0m diamond_a '
                      f'({len(diamond_a)} < {size_min_a})')
            continue
        # Diamond B
        problem_b = ProblemNeighborhood(grid=grid,
                                        start=state_b,
                                        steps_max=steps_max_b)
        bfs_b = BFSNeighborhood(problem=problem_b)
        diamond_b = list(bfs_b.run().neighborhood)
        if len(diamond_b) < size_min_b:
            log.debug(f'attempt {attempt}: '
                      f'\033[91mFAIL\033[0m diamond_b '
                      f'({len(diamond_b)} < {size_min_b})')
            continue
        random.shuffle(diamond_a)
        random.shuffle(diamond_b)
        found[0] += 1
        log.debug(f'attempt {attempt}: '
                  f'\033[92mSUCCESS\033[0m '
                  f'({len(diamond_a)}, {len(diamond_b)}) '
                  f'[{found[0]}/{n}]')
        return diamond_a, diamond_b


def get_diamonds(grid: Grid,
                 distance_min: int,
                 steps_max_a: int,
                 size_min_a: int,
                 steps_max_b: int,
                 size_min_b: int,
                 n: int) -> list[PairDiamonds]:
    """
    ========================================================================
     Get n-pairs of diamonds from the grid.
    ========================================================================
    """
    log.debug(f'get_diamonds(grid={grid.name}, n={n})')
    found = [0]
    result: list[PairDiamonds] = []
    for _ in range(n):
        pair = get_pair_diamonds(grid,
                                 distance_min,
                                 steps_max_a,
                                 size_min_a,
                                 steps_max_b,
                                 size_min_b,
                                 found=found,
                                 n=n)
        result.append(pair)
    log.debug(f'get_diamonds -> {len(result)} pairs')
    return result


def diamonds_from_grids(grids: dict[str, Grid],
                        distance_min: int,
                        steps_max_a: int,
                        size_min_a: int,
                        steps_max_b: int,
                        size_min_b: int,
                        n: int) -> DictDiamonds:
    """
    ========================================================================
     Get n-pairs of diamonds from the grids.
    ========================================================================
    """
    log.debug(f'diamonds_from_grids({len(grids)} grids, n={n})')
    d: dict[str, list[PairDiamonds]] = dict()
    for grid in grids.values():
        diamonds = get_diamonds(grid,
                                distance_min,
                                steps_max_a,
                                size_min_a,
                                steps_max_b,
                                size_min_b,
                                n)
        d[grid.name] = diamonds
    log.debug(f'diamonds_from_grids -> {len(d)} entries')
    return d


def diamonds_to_pickle(diamonds: DictDiamonds,
                       pickle_diamonds: str) -> None:
    """
    ========================================================================
     Pickle the DictDiamonds to the given path.
    ========================================================================
    """
    log.debug(f'diamonds_to_pickle({pickle_diamonds})')
    u_pickle.dump(obj=diamonds, path=pickle_diamonds)
    log.debug('diamonds_to_pickle -> done')


"""
===============================================================================
 Main - Generate Random-Pairs for a List of Grids.
 Each diamond in a pair has its own configuration (steps_max, size_min).
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid].
 Output: Pickle of dict[Grid.Name -> List[PairDiamonds]].
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_diamonds = 'f:\\temp\\2026\\03\\incremental\\diamonds.pkl'

# Number of Pairs to Generate for each Grid.
n = 100
# Minimum Distance between the Pairs.
distance_min = 100
# Diamond A Configuration
steps_max_a = 0
size_min_a = 1
# Diamond B Configuration
steps_max_b = 15
size_min_b = 100


def main(pickle_grids: str,
         pickle_diamonds: str,
         distance_min: int,
         steps_max_a: int,
         size_min_a: int,
         steps_max_b: int,
         size_min_b: int,
         n: int) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """
    log.info('main started')
    grids = load_grids(pickle_grids)
    diamonds = diamonds_from_grids(grids,
                                   distance_min,
                                   steps_max_a,
                                   size_min_a,
                                   steps_max_b,
                                   size_min_b,
                                   n)
    diamonds_to_pickle(diamonds, pickle_diamonds)
    log.info('main finished')


main(pickle_grids, pickle_diamonds, distance_min,
     steps_max_a, size_min_a, steps_max_b, size_min_b, n)
