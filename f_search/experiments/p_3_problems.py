from f_log import setup_log, get_log
from f_ds.grids import CellMap as Cell
from f_search.problems import ProblemOMSPP as Problem
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
import logging

setup_log(sink='console', level=logging.DEBUG)
log = get_log(__name__)

Diamond = list[Cell]
PairDiamonds = tuple[Diamond, Diamond]
PairsDiamonds = list[PairDiamonds]


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


def load_diamonds(pickle_diamonds: str) -> dict[str, list[Diamond]]:
    """
    ============================================================================
     Load the diamonds from the pickle file.
    ============================================================================
    """
    log.debug(f'load_diamonds({pickle_diamonds})')
    diamonds = u_pickle.load(path=pickle_diamonds)
    log.debug(f'load_diamonds -> {len(diamonds)} grids')
    return diamonds


def get_problems(d_diamonds: dict[str, list[PairsDiamonds]],
                 grids: dict[str, Grid]) -> list[Problem]:
    """
    ========================================================================
     Get the problems for the given grids and diamonds.
    ========================================================================
    """
    log.debug(f'get_problems({len(d_diamonds)} grids)')
    problems: list[Problem] = []
    for name in d_diamonds:
        grid = grids[name]
        pairs_diamonds = d_diamonds[name]
        problems_cur = _get_problems_from_grid(grid, pairs_diamonds)
        problems.extend(problems_cur)
    log.debug(f'get_problems -> {len(problems)} problems')
    return problems


def _get_problems_from_grid(grid: Grid,
                            pairs_diamonds: PairsDiamonds) -> list[Problem]:
    """
    ========================================================================
     Get the problems for the given grid and pairs of diamonds.
    ========================================================================
    """
    log.debug(f'_get_problems_from_grid(grid={grid.name})')
    problems: list[Problem] = []
    for diamond_a, diamond_b in pairs_diamonds:
        for k in k_values:
            # Problem from diamond_a to diamond_b.
            # Start = first cell of diamond_a
            # Goals = first k cells of diamond_b.
            start = diamond_a[0]
            goals = diamond_b[:k]
            problem = Problem(grid=grid, start=start, goals=goals)
            problems.append(problem)
            # Problem from diamond_b to diamond_a.
            # Start = first cell of diamond_b
            # Goals = first k cells of diamond_a.
            start = diamond_b[0]
            goals = diamond_a[:k]
            problem = Problem(grid=grid, start=start, goals=goals)
            problems.append(problem)
    log.debug(f'_get_problems_from_grid -> {len(problems)} problems')
    return problems


def pickle_results(problems: dict[str, list[Problem]],
                   pickle_problems: str) -> None:
    """
    ============================================================================
     Pickle the results to the given path.
    ============================================================================
    """
    log.debug(f'pickle_results({pickle_problems})')
    u_pickle.dump(obj=problems, path=pickle_problems)
    log.debug('pickle_results -> done')


"""
===============================================================================
 Main - Generate the problems for a list of grids and pairs.
 For each pair we generate two problems (in both directions).
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid], dict[Grid.Name -> List[Pair]].
 Output: Pickle of dict[Grid.Name -> List[Problem]].
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
folder = 'f:\\temp\\2026\\03\\Forward vs Backward'
pickle_diamonds = f'{folder}\\diamonds.pkl'
pickle_problems = f'{folder}\\problems.pkl'

k_values = [2, 4, 6, 8, 10]


def main() -> None:
    log.info('main started')
    grids = load_grids(pickle_grids)
    d_diamonds = load_diamonds(pickle_diamonds)
    problems = get_problems(d_diamonds, grids=grids)
    pickle_results(problems, pickle_problems)
    log.info('main finished')


main()
