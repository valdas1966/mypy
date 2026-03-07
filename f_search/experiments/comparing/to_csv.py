import logging
import csv
from itertools import combinations
from f_log import setup_log
from f_search.problems import ProblemOMSPP
from f_search.solutions import SolutionOMSPP
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle


def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ========================================================================
     Load the grids from the pickle file.
    ========================================================================
    """
    logging.info(f'Loading grids from {pickle_grids}')
    grids = u_pickle.load(path=pickle_grids)
    logging.info(f'Loaded {len(grids)} grids')
    return grids


def load_solutions(path: str) -> list[SolutionOMSPP]:
    """
    ========================================================================
     Load solutions from a pickle file.
    ========================================================================
    """
    logging.info(f'Loading solutions from {path}')
    solutions = u_pickle.load(path=path)
    logging.info(f'Loaded {len(solutions)} solutions')
    return solutions


def _avg_dist_start_to_goals(problem: ProblemOMSPP) -> float:
    """
    ========================================================================
     Average Manhattan distance from start to each goal.
    ========================================================================
    """
    start = problem.start
    dists = [start.distance(g) for g in problem.goals]
    return sum(dists) / len(dists)


def _avg_dist_between_goals(problem: ProblemOMSPP) -> float:
    """
    ========================================================================
     Average pairwise Manhattan distance between goals.
    ========================================================================
    """
    goals = problem.goals
    if len(goals) < 2:
        return 0.0
    pairs = list(combinations(goals, 2))
    dists = [a.distance(b) for a, b in pairs]
    return sum(dists) / len(dists)


def _avg_heuristic_efficiency(solution: SolutionOMSPP) -> float:
    """
    ========================================================================
     Average heuristic efficiency across all sub-searches.
     Efficiency = manhattan(start, goal) / path_cost * 100.
     A perfect heuristic yields 100%.
    ========================================================================
    """
    efficiencies = []
    for sub in solution.subs:
        if not sub.is_valid or sub.path is None:
            continue
        h = sub.problem.start.distance(sub.problem.goal)
        g = len(sub.path.to_iterable()) - 1
        if g > 0:
            efficiencies.append(h / g * 100)
    if not efficiencies:
        return 0.0
    return sum(efficiencies) / len(efficiencies)


def merge_to_csv(d_grids: dict[str, Grid],
                 forward: list[SolutionOMSPP],
                 backward: list[SolutionOMSPP],
                 path_csv: str) -> None:
    """
    ========================================================================
     Merge forward and backward solutions into a single CSV.
    ========================================================================
    """
    fieldnames = ['domain', 'map', 'grid_rows', 'grid_cols',
                  'grid_cells', 'k', 'avg_dist_start_goals',
                  'avg_dist_between_goals',
                  'norm_dist_start_goals',
                  'norm_dist_between_goals',
                  'forward_heuristic', 'backward_heuristic',
                  'forward_explored', 'backward_explored',
                  'forward_elapsed', 'backward_elapsed']
    with open(path_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for fwd, bwd in zip(forward, backward):
            problem = fwd.problem
            grid_name = problem.name_grid
            grid = d_grids[grid_name]
            cells = len(grid)
            avg_sg = _avg_dist_start_to_goals(problem)
            avg_gg = _avg_dist_between_goals(problem)
            writer.writerow({
                'domain': grid.domain,
                'map': grid_name,
                'grid_rows': grid.rows,
                'grid_cols': grid.cols,
                'grid_cells': cells,
                'k': len(problem.goals),
                'avg_dist_start_goals': round(avg_sg, 2),
                'avg_dist_between_goals': round(avg_gg, 2),
                'norm_dist_start_goals':
                    round(avg_sg / cells * 100, 2),
                'norm_dist_between_goals':
                    round(avg_gg / cells * 100, 2),
                'forward_heuristic':
                    round(_avg_heuristic_efficiency(fwd), 2),
                'backward_heuristic':
                    round(_avg_heuristic_efficiency(bwd), 2),
                'forward_explored': fwd.stats.explored,
                'backward_explored': bwd.stats.explored,
                'forward_elapsed': fwd.stats.elapsed,
                'backward_elapsed': bwd.stats.elapsed,
            })
    logging.info(f'Wrote {len(forward)} rows to {path_csv}')


"""
===============================================================================
 Main - Convert forward and backward pickle files into a comparison CSV.
-------------------------------------------------------------------------------
 Input: Pickle of grids, Pickle of forward solutions, Pickle of backward.
 Output: CSV with grid metadata, problem features, and performance metrics.
===============================================================================
"""

setup_log()

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
dir_exp = 'f:\\temp\\2026\\03\\Exp Depth'
pickle_forward = f'{dir_exp}\\forward.pkl'
pickle_backward = f'{dir_exp}\\backward.pkl'
path_csv = f'{dir_exp}\\forward_vs_backward.csv'

d_grids = load_grids(pickle_grids)
forward = load_solutions(path=pickle_forward)
backward = load_solutions(path=pickle_backward)
merge_to_csv(d_grids=d_grids,
             forward=forward,
             backward=backward,
             path_csv=path_csv)
