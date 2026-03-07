import logging
from f_log import setup_log
from f_search.algos.i_2_omspp.i_1_incremental.astar import (
    AStarIncremental)
from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.problems import ProblemOMSPP
from f_search.solutions import SolutionOMSPP
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
from typing import Any


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


def load_problems(pickle_problems: str) -> list[ProblemOMSPP]:
    """
    ========================================================================
     Load the problems from the pickle file.
    ========================================================================
    """
    logging.info(f'Loading problems from {pickle_problems}')
    problems = u_pickle.load(path=pickle_problems)
    logging.info(f'Loaded {len(problems)} problems')
    return problems


def run_algo(type_algo: type[AlgoOMSPP],
             d_grids: dict[str, Grid],
             problems: list[ProblemOMSPP],
             **algo_kwargs: Any) -> list[SolutionOMSPP]:
    """
    ========================================================================
     Run an OMSPP algorithm on each problem and return solutions.
    ========================================================================
    """
    total = len(problems)
    logging.info(f'Running {type_algo.__name__} on {total} problems')
    solutions: list[SolutionOMSPP] = []
    for i, problem in enumerate(problems):
        problem.load_grid(grids=d_grids)
        algo = type_algo(problem=problem, **algo_kwargs)
        solution = algo.run()
        solutions.append(solution)
        logging.info(f'Problem {i+1}/{total} '
                     f'explored={solution.stats.explored}')
    logging.info(f'Finished {type_algo.__name__}')
    return solutions


def pickle_result(solutions: list[SolutionOMSPP],
                  path: str) -> None:
    """
    ========================================================================
     Pickle the solutions to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=solutions, path=path)
    logging.info(f'Pickled {len(solutions)} solutions to {path}')


"""
===============================================================================
 Main - Run forward and backward incremental A* on pre-generated problems.
-------------------------------------------------------------------------------
 Input: Pickle of grids, Pickle of problems.
 Output: Pickle of forward solutions, Pickle of backward solutions.
===============================================================================
"""

setup_log()

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
dir_exp = 'f:\\temp\\2026\\03'
pickle_problems = f'{dir_exp}\\Exp Depth\\problems.pkl'
pickle_forward = f'{dir_exp}\\forward.pkl'
pickle_backward = f'{dir_exp}\\backward.pkl'

d_grids = load_grids(pickle_grids)
problems = load_problems(pickle_problems)

# Forward incremental A*
forward = run_algo(AStarIncremental, d_grids, problems)
pickle_result(forward, pickle_forward)

# Backward incremental A* (with bounds)
backward = run_algo(AStarIncrementalBackward, d_grids, problems,
                    with_bounds=True)
pickle_result(backward, pickle_backward)
