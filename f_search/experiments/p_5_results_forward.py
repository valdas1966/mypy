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
            sols_agg: list[SolutionOMSPP],
            sols_inc: list[SolutionOMSPP]#,
            #sols_dij: list[SolutionOMSPP],
            #sols_bfs: list[SolutionOMSPP]
            ) -> list[dict]:
    """
    ========================================================================
     Merge aggregative, incremental, dijkstra and repeated solutions.
    ========================================================================
    """
    log.debug(f'to_rows({len(sols_agg)} agg, '
              f'{len(sols_inc)} inc, '
              #f'{len(sols_dij)} dij, '
              #f'{len(sols_bfs)} bfs)'
             )
    rows: list[dict] = []
    #for i, (agg, inc, dij, bfs) in enumerate(zip(sols_agg, sols_inc)):  # , sols_dij, sols_bfs)):
    for i, (agg, inc) in enumerate(zip(sols_agg, sols_inc)):
        problem: ProblemOMSPP = agg.problem
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
            explored_agg=agg.stats.explored,
            explored_inc=inc.stats.explored,
            #explored_dij=dij.stats.explored,
            #explored_bfs=bfs.stats.explored,
            elapsed_agg=agg.stats.elapsed,
            elapsed_inc=inc.stats.elapsed,
            #elapsed_dij=dij.stats.elapsed,
            #elapsed_bfs=bfs.stats.elapsed
            cnt_h_agg=agg.stats.heuristic_calcs,
            cnt_h_inc=inc.stats.heuristic_calcs
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
 Main - Merge aggregative, incremental, dijkstra and repeated solutions.
-------------------------------------------------------------------------------
 Input: Pickle of grids, aggregative, incremental, dijkstra and bfs.
 Output: CSV with merged analytics.
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
folder = 'f:\\temp\\2026\\03\\calch'
pickle_agg = f'{folder}\\aggregative.pkl'
pickle_inc = f'{folder}\\incremental.pkl'
#pickle_dij = f'{folder}\\dijkstra.pkl'
#pickle_bfs = f'{folder}\\bfs.pkl'
path_csv = f'{folder}\\results.csv'


def main() -> None:
    log.info('main started')
    grids = load_grids(pickle_grids)
    sols_agg = load_solutions(pickle_agg)
    sols_inc = load_solutions(pickle_inc)
    #sols_dij = load_solutions(pickle_dij)
    #sols_bfs = load_solutions(pickle_bfs)
    rows = to_rows(grids, sols_agg, sols_inc) #, sols_dij, sols_bfs)
    to_csv(rows, path_csv)
    log.info(f'main finished -> {path_csv}')


main()
