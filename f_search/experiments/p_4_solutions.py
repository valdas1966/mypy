from f_log import setup_log, get_log
from f_search.algos.i_1_spp import Dijkstra
from f_search.problems import ProblemOMSPP
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_2_omspp import AStarRepeated
from f_search.algos.i_2_omspp import BFSIncremental
from f_search.algos.i_2_omspp import AStarIncremental
from f_search.algos.i_2_omspp import DijkstraIncremental
from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative
from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import AStarIncrementalBackward
from f_search.solutions import SolutionOMSPP
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle
from typing import Any
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


def load_problems(pickle_problems: str) -> list[ProblemOMSPP]:
    """
    ========================================================================
     Load the problems from the pickle file.
    ========================================================================
    """
    log.debug(f'load_problems({pickle_problems})')
    problems = u_pickle.load(path=pickle_problems)
    log.debug(f'load_problems -> {len(problems)} problems')
    return problems


def run_algos(type_algo: type[AlgoOMSPP],
              d_grids: dict[str, Grid],
              problems: list[ProblemOMSPP],
              **algo_kwargs: Any) -> list[SolutionOMSPP]:
    """
    ========================================================================
     Run the algorithms for the given problems.
    ========================================================================
    """
    log.debug(f'run_algos({type_algo.__name__}, {len(problems)} problems)')
    solutions: list[SolutionOMSPP] = []
    for i, problem in enumerate(problems):
        problem.load_grid(grids=d_grids)
        solution = _run_problem(type_algo, problem, i, **algo_kwargs)
        solutions.append(solution)
    log.debug(f'run_algos -> {len(solutions)} solutions')
    return solutions


def _run_problem(type_algo: type[AlgoOMSPP],
                 problem: ProblemOMSPP,
                 i: int,
                 **algo_kwargs: Any) -> SolutionOMSPP:
    """
    ========================================================================
     Run the algorithm for the given problem.
    ========================================================================
    """
    log.debug(f'_run_problem({type_algo.__name__}, i={i})')
    algo = type_algo(problem=problem, **algo_kwargs)
    return algo.run()


def pickle_result(solutions: list[SolutionOMSPP],
                  pickle_solutions: str) -> None:
    """
    ========================================================================
     Pickle the solutions to the given path.
    ========================================================================
    """
    log.debug(f'pickle_result({pickle_solutions})')
    u_pickle.dump(obj=solutions, path=pickle_solutions)
    log.debug('pickle_result -> done')


"""
===============================================================================
 Main - Load the grids and problems.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid], Pickle of list[ProblemOMSPP].
 Output: None.
===============================================================================
"""

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
folder = 'f:\\temp\\2026\\03\\Forward vs Backward'
pickle_problems = f'{folder}\\problems.pkl'
pickle_solutions = f'{folder}\\forward.pkl'

algo = AStarIncremental
#algo = AStarIncrementalBackward

d_grids = load_grids(pickle_grids)
problems = load_problems(pickle_problems)
# solutions = run_algos(algo, d_grids, problems, with_bounds=True, need_path=True)
solutions = run_algos(algo, d_grids, problems, need_path=True)
pickle_result(solutions, pickle_solutions)
