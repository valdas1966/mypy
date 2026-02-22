from f_log.old.utils import set_debug, log_2
from f_search.algos.i_1_spp import Dijkstra
from f_search.problems import ProblemOMSPP
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_2_omspp import AStarRepeated
from f_search.algos.i_2_omspp import BFSIncremental
from f_search.algos.i_2_omspp import AStarIncremental
from f_search.algos.i_2_omspp import DijkstraIncremental
from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative
from f_search.solutions import SolutionOMSPP
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ========================================================================
     Load the grids from the pickle file.
    ========================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_2
def load_problems(pickle_problems: str) -> list[ProblemOMSPP]:
    """
    ========================================================================
     Load the problems from the pickle file.
    ========================================================================
    """
    return u_pickle.load(path=pickle_problems)


@log_2
def run_algos(type_algo: type[AlgoOMSPP],
              d_grids: dict[str, Grid],
              problems: list[ProblemOMSPP]) -> list[SolutionOMSPP]:
    """
    ========================================================================
     Run the algorithms for the given problems.
    ========================================================================
    """
    solutions: list[SolutionOMSPP] = []
    for i, problem in enumerate(problems):
        problem = problem.to_heavy(grids=d_grids)
        solution = _run_problem(type_algo, problem, i)
        solutions.append(solution)
    return solutions

@log_2
def pickle_result(solutions: list[SolutionOMSPP], pickle_solutions: str) -> None:
    """
    ========================================================================
     Pickle the solutions to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=solutions, path=pickle_solutions)


@log_2
def _run_problem(type_algo: type[AlgoOMSPP],
                 problem: ProblemOMSPP,
                 i: int) -> SolutionOMSPP:
    """
    ========================================================================
     Run the algorithm for the given problem.
    ========================================================================
    """
    algo = type_algo(problem=problem)
    return algo.run()


"""
===============================================================================
 Main - Load the grids and problems.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid], Pickle of list[ProblemOMSPP].
 Output: None.
===============================================================================
"""

set_debug(True)

pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_problems = 'f:\\paper\\i_3_problems\\problems.pkl'

algo = DijkstraIncremental
pickle_solutions = f'f:\\paper\\i_4_solutions\\dijkstra.pkl'

d_grids = load_grids(pickle_grids)
problems = load_problems(pickle_problems)
solutions = run_algos(algo, d_grids, problems)
pickle_result(solutions, pickle_solutions)
