import pandas as pd
from f_log import setup_log, get_log
from f_search.problems import ProblemOMSPP as Problem
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
import logging

setup_log(sink='console', level=logging.DEBUG)
log = get_log(__name__)


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


def load_problems(pickle_problems: str,
                  grids: dict[str, Grid]) -> list[Problem]:
    """
    ========================================================================
     Load the problems and restore their grids.
    ========================================================================
    """
    log.debug(f'load_problems({pickle_problems})')
    problems = u_pickle.load(path=pickle_problems)
    for problem in problems:
        problem.load_grid(grids=grids)
    log.debug(f'load_problems -> {len(problems)} problems')
    return problems


def problems_to_csv(problems: list[Problem],
                    path_csv: str) -> None:
    """
    ========================================================================
     Convert the problems to a CSV file with analytics.
    ========================================================================
    """
    log.debug(f'problems_to_csv({path_csv})')
    rows: list[dict] = []
    for problem in problems:
        analytics = problem.to_analytics()
        start = problem.start
        goal = problem.goals[0]
        row = analytics | {
            'k': len(problem.goals),
            'row_start': start.key.row,
            'col_start': start.key.col,
            'row_goal': goal.key.row,
            'col_goal': goal.key.col,
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(path_csv, index=False)
    log.debug(f'problems_to_csv -> {len(df)} rows')


"""
===============================================================================
 Main - Convert problems.pkl to analytics CSV.
-------------------------------------------------------------------------------
 Input: Pickle of grids, Pickle of problems.
 Output: CSV with analytics for each problem.
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_problems = 'f:\\temp\\2026\\03\\forward vs backward\\problems.pkl'
path_csv = pickle_problems.replace('.pkl', '.csv')


def main() -> None:
    log.info('main started')
    grids = load_grids(pickle_grids)
    problems = load_problems(pickle_problems, grids=grids)
    problems_to_csv(problems, path_csv=path_csv)
    log.info('main finished')


main()
