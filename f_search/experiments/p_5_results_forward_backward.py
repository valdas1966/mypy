from f_log import setup_log, get_log
from f_search.solutions import SolutionOMSPP
from f_search.problems import ProblemOMSPP
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
import logging
import csv

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


def load_solutions(pickle_path: str) -> list[SolutionOMSPP]:
    """
    ========================================================================
     Load the solutions from the pickle file.
    ========================================================================
    """
    log.debug(f'load_solutions({pickle_path})')
    solutions = u_pickle.load(path=pickle_path)
    log.debug(f'load_solutions -> {len(solutions)} solutions')
    return solutions


def to_rows(grids: dict[str, Grid],
            sols_fwd: list[SolutionOMSPP],
            sols_bwd: list[SolutionOMSPP]) -> list[dict]:
    """
    ========================================================================
     Merge forward and backward solutions into rows for CSV.
    ========================================================================
    """
    log.debug(f'to_rows({len(sols_fwd)} forward, {len(sols_bwd)} backward)')
    rows: list[dict] = []
    for i, (fwd, bwd) in enumerate(zip(sols_fwd, sols_bwd)):
        problem: ProblemOMSPP = fwd.problem
        problem.load_grid(grids=grids)
        analytics = problem.to_analytics()
        row = dict(
            index=i,
            domain=analytics['domain'],
            map=analytics['map'],
            rows=analytics['rows'],
            cols=analytics['cols'],
            cells=analytics['cells'],
            k=len(problem.goals),
            h_start=analytics['h_start'],
            norm_h_start=analytics['norm_h_start'],
            h_goals=analytics['h_goals'],
            norm_h_goals=analytics['norm_h_goals'],
            quality_h_forward=fwd.quality_h,
            quality_h_backward=bwd.quality_h,
            explored_forward=fwd.stats.explored,
            explored_backward=bwd.stats.explored,
            elapsed_forward=fwd.stats.elapsed,
            elapsed_backward=bwd.stats.elapsed,
        )
        rows.append(row)
    log.debug(f'to_rows -> {len(rows)} rows')
    return rows


def to_csv(rows: list[dict], path_csv: str) -> None:
    """
    ========================================================================
     Write the rows to a CSV file.
    ========================================================================
    """
    log.debug(f'to_csv({path_csv})')
    fieldnames = list(rows[0].keys())
    with open(path_csv, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.debug(f'to_csv -> {len(rows)} rows written')


"""
===============================================================================
 Main - Merge forward and backward solutions into a CSV.
-------------------------------------------------------------------------------
 Input: Pickle of grids, forward solutions, backward solutions.
 Output: CSV with merged analytics.
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
folder = 'f:\\temp\\2026\\03\\Forward vs Backward'
pickle_forward = f'{folder}\\forward.pkl'
pickle_backward = f'{folder}\\backward.pkl'
path_csv = f'{folder}\\results.csv'


def main() -> None:
    log.info('main started')
    grids = load_grids(pickle_grids)
    sols_fwd = load_solutions(pickle_forward)
    sols_bwd = load_solutions(pickle_backward)
    rows = to_rows(grids, sols_fwd, sols_bwd)
    to_csv(rows, path_csv)
    log.info(f'main finished -> {path_csv}')


main()
