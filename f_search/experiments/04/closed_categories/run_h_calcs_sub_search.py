"""
============================================================================
 Run Incremental-kA* on 5000 ProblemOMSPP instances.
 Write sub-search heuristic calcs (excluding re-keying) to CSV
 and upload to Google Drive.
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
from f_google.services.drive import Drive

PATH_GRIDS = 'f:\\paper\\i_1_grids\\grids.pkl'
PATH_PROBLEMS = ('f:\\temp\\2026\\04\\'
                 'closed categories\\problems.pkl')
PATH_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'results_h_calcs_sub_search.csv')
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
     Run Incremental-kA* and return sub-search heuristic calcs
     (discovered during sub-search, excluding re-keying).
    ========================================================================
    """
    from f_search.algos.i_2_omspp import AStarIncremental
    problem.load_grid(grids=_worker_grids)
    algo = AStarIncremental(problem=problem)
    solution = algo.run()
    # Total heuristic_calcs = re-keying + discovered
    # Sub-search h-calcs only = discovered (1 h-calc per discovery)
    return solution.stats.discovered


def main():
    """
    ========================================================================
     Load problems, run Incremental-kA* in parallel, write and upload.
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
        writer.writerow(['h_calcs_sub_search_inc'])
        for val in results:
            writer.writerow([val])
    print(f'Results saved to {PATH_RESULTS}')
    # Upload to Google Drive
    drive = Drive.Factory.valdas()
    path_dest = '2026/04/closed_categories/results_h_calcs_sub_search.csv'
    drive.upload(path_src=PATH_RESULTS, path_dest=path_dest)
    print(f'Uploaded to {path_dest}')


if __name__ == '__main__':
    main()
