from f_log import setup_log, get_log
from f_ds.grids import CellMap as Cell
from f_search.problems import ProblemOMSPP as Problem
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
import logging
import random

setup_log(sink='console', level=logging.DEBUG)
log = get_log(__name__)

Diamond = list[Cell]
PairDiamonds = tuple[Diamond, Diamond]
PairsDiamonds = list[PairDiamonds]


def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ========================================================================
     Load the grids from the pickle file.
    ========================================================================
    """
    log.debug(f'load_grids({pickle_grids})')
    grids = u_pickle.load(path=pickle_grids)
    log.debug(f'load_grids -> {len(grids)} grids')
    return grids


def load_diamonds(pickle_diamonds: str) -> dict[str, list[Diamond]]:
    """
    ========================================================================
     Load the diamonds from the pickle file.
    ========================================================================
    """
    log.debug(f'load_diamonds({pickle_diamonds})')
    diamonds = u_pickle.load(path=pickle_diamonds)
    log.debug(f'load_diamonds -> {len(diamonds)} grids')
    return diamonds


def _problem_from_pair(grid: Grid,
                       diamond_a: Diamond,
                       diamond_b: Diamond,
                       k: int) -> Problem:
    """
    ========================================================================
     Create one OMSPP Problem from a pair of diamonds.
     Start = first cell of diamond_a.
     Goals = k randomly chosen cells from diamond_b.
    ========================================================================
    """
    start = diamond_a[0]
    goals = random.sample(diamond_b, k=k)
    return Problem(grid=grid, start=start, goals=goals)


def _get_problems_from_grid(grid: Grid,
                            pairs_diamonds: PairsDiamonds,
                            values_k: list[int]) -> list[Problem]:
    """
    ========================================================================
     Distribute diamond pairs evenly across k-values.
     E.g. 100 pairs with values_k=[2,4,6,8,10] -> 20 per k-value.
    ========================================================================
    """
    log.debug(f'_get_problems_from_grid(grid={grid.name})')
    n = len(pairs_diamonds)
    n_k = len(values_k)
    chunk = n // n_k
    problems: list[Problem] = []
    for i, k in enumerate(values_k):
        start_idx = i * chunk
        # Last k-value gets the remainder
        if i == n_k - 1:
            end_idx = n
        else:
            end_idx = start_idx + chunk
        for diamond_a, diamond_b in pairs_diamonds[start_idx:end_idx]:
            if len(diamond_b) >= k:
                problem = _problem_from_pair(grid,
                                             diamond_a,
                                             diamond_b,
                                             k)
                problems.append(problem)
    log.debug(f'_get_problems_from_grid -> {len(problems)} problems')
    return problems


def get_problems(d_diamonds: dict[str, list[PairsDiamonds]],
                 grids: dict[str, Grid],
                 values_k: list[int]) -> list[Problem]:
    """
    ========================================================================
     Get one Problem per diamond pair for all grids.
     Diamond pairs are distributed evenly across k-values.
    ========================================================================
    """
    log.debug(f'get_problems({len(d_diamonds)} grids, '
              f'values_k={values_k})')
    problems: list[Problem] = []
    for name in d_diamonds:
        grid = grids[name]
        pairs_diamonds = d_diamonds[name]
        problems_cur = _get_problems_from_grid(grid,
                                               pairs_diamonds,
                                               values_k)
        problems.extend(problems_cur)
    log.debug(f'get_problems -> {len(problems)} problems')
    return problems


def pickle_results(problems: list[Problem],
                   pickle_problems: str) -> None:
    """
    ========================================================================
     Pickle the results to the given path.
    ========================================================================
    """
    log.debug(f'pickle_results({pickle_problems})')
    u_pickle.dump(obj=problems, path=pickle_problems)
    log.debug('pickle_results -> done')


"""
===============================================================================
 Main - Generate OMSPP Problems from Diamond Pairs.
 Start = diamond_a (single cell), Goals = k random cells from diamond_b.
 Diamond pairs are distributed evenly across k-values.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid],
        dict[Grid.Name -> List[PairDiamonds]].
 Output: Pickle of List[Problem].
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
folder = 'f:\\temp\\2026\\03\\forward vs backward'
pickle_diamonds = f'{folder}\\diamonds.pkl'
pickle_problems = f'{folder}\\problems.pkl'

# values_k = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values_k = [2, 4, 6, 8, 10]


def main() -> None:
    log.info('main started')
    grids = load_grids(pickle_grids)
    d_diamonds = load_diamonds(pickle_diamonds)
    problems = get_problems(d_diamonds, grids=grids,
                            values_k=values_k)
    pickle_results(problems, pickle_problems)
    log.info('main finished')


main()
