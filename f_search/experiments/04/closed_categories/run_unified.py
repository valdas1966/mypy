"""
============================================================================
 Run Incremental-kA* and Aggregative-kA* on 5000 ProblemOMSPP instances.
 Collect ALL metrics in a single pass: problem metadata, algorithm
 stats (explored, elapsed, discovered, h_calcs), and node categories
 (surely, borderline, surplus).
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
PATH_TMP = os.path.join(os.environ.get('TEMP', '/tmp'),
                        'results_unified.csv')
PATH_DRIVE = '2026/04/Experiments/OMSPP/results_unified.csv'
WORKERS = 11

HEADER = [
    # Problem metadata
    'index', 'domain', 'map', 'rows', 'cols', 'cells', 'k',
    'h_start', 'norm_h_start', 'h_goals', 'norm_h_goals',
    # Incremental stats
    'explored_inc', 'elapsed_inc', 'discovered_inc', 'h_calcs_inc',
    # Aggregative stats
    'explored_agg', 'elapsed_agg', 'discovered_agg', 'h_calcs_agg',
    # Incremental categories
    'surely_inc', 'border_inc', 'surplus_inc',
    # Aggregative categories
    'surely_agg', 'border_agg', 'surplus_agg',
]

_worker_grids = None


def init_worker(path_grids: str) -> None:
    """
    ========================================================================
     Load grids once per worker process.
    ========================================================================
    """
    global _worker_grids
    _worker_grids = u_pickle.load(path=path_grids)


def process_problem(args: tuple) -> dict:
    """
    ========================================================================
     Run both algorithms on a single problem and return all metrics.
    ========================================================================
    """
    from f_search.algos.i_2_omspp import (AStarIncremental,
                                           AStarAggregative)
    index, problem = args
    problem.load_grid(grids=_worker_grids)
    # Problem metadata
    analytics = problem.to_analytics()
    k = len(problem.goals)
    # Incremental kA*
    algo_inc = AStarIncremental(problem=problem)
    sol_inc = algo_inc.run()
    cats_inc = algo_inc.closed_categories()
    s_inc = len(cats_inc['Surely Expanded'])
    b_inc = len(cats_inc['Borderline'])
    p_inc = len(cats_inc['Surplus'])
    # Sanity check
    assert s_inc + b_inc + p_inc == sol_inc.stats.explored, (
        f'Problem {index}: categories ({s_inc}+{b_inc}+{p_inc}'
        f'={s_inc+b_inc+p_inc}) != explored '
        f'({sol_inc.stats.explored})')
    # Aggregative kA*
    algo_agg = AStarAggregative(problem=problem)
    sol_agg = algo_agg.run()
    cats_agg = algo_agg.closed_categories()
    s_agg = len(cats_agg['Surely Expanded'])
    b_agg = len(cats_agg['Borderline'])
    p_agg = len(cats_agg['Surplus'])
    # Sanity check
    assert s_agg + b_agg + p_agg == sol_agg.stats.explored, (
        f'Problem {index}: categories ({s_agg}+{b_agg}+{p_agg}'
        f'={s_agg+b_agg+p_agg}) != explored '
        f'({sol_agg.stats.explored})')
    return {
        'index': index,
        'domain': analytics['domain'],
        'map': analytics['map'],
        'rows': analytics['rows'],
        'cols': analytics['cols'],
        'cells': analytics['cells'],
        'k': k,
        'h_start': analytics['h_start'],
        'norm_h_start': analytics['norm_h_start'],
        'h_goals': analytics['h_goals'],
        'norm_h_goals': analytics['norm_h_goals'],
        'explored_inc': sol_inc.stats.explored,
        'elapsed_inc': sol_inc.stats.elapsed,
        'discovered_inc': sol_inc.stats.discovered,
        'h_calcs_inc': sol_inc.stats.heuristic_calcs,
        'explored_agg': sol_agg.stats.explored,
        'elapsed_agg': sol_agg.stats.elapsed,
        'discovered_agg': sol_agg.stats.discovered,
        'h_calcs_agg': sol_agg.stats.heuristic_calcs,
        'surely_inc': s_inc,
        'border_inc': b_inc,
        'surplus_inc': p_inc,
        'surely_agg': s_agg,
        'border_agg': b_agg,
        'surplus_agg': p_agg,
    }


def main():
    """
    ========================================================================
     Load problems, run both algorithms in parallel, write unified CSV.
    ========================================================================
    """
    with open(PATH_PROBLEMS, 'rb') as f:
        problems = pickle.load(f)
    print(f'Loaded {len(problems)} problems')
    results = [None] * len(problems)
    with ProcessPoolExecutor(max_workers=WORKERS,
                             initializer=init_worker,
                             initargs=(PATH_GRIDS,)) as executor:
        futures = {
            executor.submit(process_problem, (i, p)): i
            for i, p in enumerate(problems)
        }
        for future in tqdm(as_completed(futures),
                           total=len(problems),
                           desc='Running'):
            i = futures[future]
            results[i] = future.result()
    with open(PATH_TMP, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(results)
    # Upload to Drive
    drive = Drive.Factory.valdas()
    drive.upload(path_src=PATH_TMP, path_dest=PATH_DRIVE)
    print(f'Uploaded to {PATH_DRIVE}')
    # Summary
    total = len(results)
    explored = sum(r['explored_inc'] for r in results)
    surely = sum(r['surely_inc'] for r in results)
    border = sum(r['border_inc'] for r in results)
    print(f'Total problems: {total}')
    print(f'Avg explored (inc): {explored/total:.0f}')
    print(f'Surely %: {100*surely/(surely+border):.1f}%')
    print(f'Border %: {100*border/(surely+border):.1f}%')


if __name__ == '__main__':
    main()
