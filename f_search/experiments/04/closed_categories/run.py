"""
============================================================================
 Run Incremental-kA* and Aggregative-kA* on 5000 ProblemOMSPP instances.
 Write closed_categories() counts to results.csv.
============================================================================
"""
import sys
import os
import pickle
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..', '..', '..')))

from f_utils import u_pickle

PATH_GRIDS = 'f:\\paper\\i_1_grids\\grids.pkl'
PATH_PROBLEMS = ('f:\\temp\\2026\\04\\'
                 'closed categories\\problems.pkl')
PATH_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'results.csv')
WORKERS = 11

_worker_grids = None


def init_worker(path_grids: str) -> None:
    """
    ========================================================================
     Load grids once per worker process.
    ========================================================================
    """
    global _worker_grids
    _worker_grids = u_pickle.load(path=path_grids)


def process_problem(problem):
    """
    ========================================================================
     Run both algorithms on a single problem and return category counts.
    ========================================================================
    """
    from f_search.algos.i_2_omspp import (AStarIncremental,
                                           AStarAggregative)
    problem.load_grid(grids=_worker_grids)
    # Incremental kA*
    algo_inc = AStarIncremental(problem=problem)
    algo_inc.run()
    cats_inc = algo_inc.closed_categories()
    # Aggregative kA*
    algo_agg = AStarAggregative(problem=problem)
    algo_agg.run()
    cats_agg = algo_agg.closed_categories()
    return (len(cats_inc['Surely Expanded']),
            len(cats_agg['Surely Expanded']),
            len(cats_inc['Borderline']),
            len(cats_agg['Borderline']),
            len(cats_inc['Surplus']),
            len(cats_agg['Surplus']))


def main():
    """
    ========================================================================
     Load problems, run both algorithms in parallel, write results.csv.
    ========================================================================
    """
    with open(PATH_PROBLEMS, 'rb') as f:
        problems = pickle.load(f)
    print(f'Loaded {len(problems)} problems')
    results = [None] * len(problems)
    with ProcessPoolExecutor(max_workers=WORKERS,
                             initializer=init_worker,
                             initargs=(PATH_GRIDS,)) as executor:
        futures = {executor.submit(process_problem, p): i
                   for i, p in enumerate(problems)}
        for future in tqdm(as_completed(futures),
                           total=len(problems),
                           desc='Running'):
            i = futures[future]
            results[i] = future.result()
    with open(PATH_RESULTS, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['surely_inc', 'surely_agg',
                         'border_inc', 'border_agg',
                         'surplus_inc', 'surplus_agg'])
        writer.writerows(results)
    print(f'Results saved to {PATH_RESULTS}')


if __name__ == '__main__':
    main()
