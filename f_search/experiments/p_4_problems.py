from f_log.utils import set_debug, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.algos.i_1_spp.utils import random_cells_up_to_distance
from f_search.problems import ProblemOMSPPLite as ProblemLite
from f_search.ds.states import StateCell as State
from f_utils import u_pickle
import random

Pair = tuple[Cell, Cell]


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)

@log_2
def load_pairs(pickle_pairs: str) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Load the pairs from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_pairs)


@log_2
def gen_problems(grids: dict[str, Grid],
                 pairs: dict[str, list[Pair]],
                 k_max: int,
                 distance_rect: int,
                 distance_path_max: int,
                 tries: int) -> dict[str, list[ProblemLite]]:
    """
    ============================================================================
     Generate the problems from the pairs.
    ============================================================================
    """
    @log_2
    def for_grid(grid: Grid,
                 pairs: list[Pair],
                 total: int,
                 i: int) -> list[ProblemLite]:
        """
        ============================================================================
         Generate the problems for a given grid.
        ============================================================================
        """
        def gen_problem(start: Cell,
                        candidates_goals: list[Cell]) -> ProblemLite:
            """
            ========================================================================
             Generate a problem with a given start, candidates goals, and k.
            ========================================================================
            """
            start = State(key=start)
            cells_goals = random_cells_up_to_distance(grid=grid,
                                                      cells=candidates_goals,
                                                      distance=distance_path_max,
                                                      k=k_max,
                                                      tries=tries)
            goals = [State(key=cell) for cell in cells_goals]
            return ProblemLite(grid=grid.name, start=start, goals=goals)

        problems: list[ProblemLite] = []
        for a, b in pairs:
            # Generate the problem from A to B.
            rect_b = grid.select.rect_around(cell=b, distance=distance_rect)
            problem_ab = gen_problem(start=a, candidates_goals=list(rect_b))
            problems.append(problem_ab)
            # Generate the problem from B to A.
            rect_a = grid.select.rect_around(cell=a, distance=distance_rect)
            problem_ba = gen_problem(start=b, candidates_goals=list(rect_a))
            problems.append(problem_ba)
        return problems

    total = len(grids)
    d: dict[str, list[ProblemLite]] = dict()
    for i, (name, grid) in enumerate(grids.items()):
        problems = for_grid(grid=grid, pairs=pairs[name], total=total, i=i+1)
        d[name] = problems
    return d

@log_2
def pickle_results(problems: dict[str, list[ProblemLite]],
                   pickle_problems: str) -> None:
    """
    ============================================================================
     Pickle the results to the given path.
    ============================================================================
    """
    u_pickle.dump(obj=problems, path=pickle_problems)


"""
===============================================================================
 Main - Generate the problems for a list of grids and pairs.
 For each pair we generate two problems (in both directions).
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name -> Grid], dict[Grid.Name -> List[Pair]].
 Output: Pickle of dict[Grid.Name -> List[ProblemLite]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_pairs = 'f:\\paper\\i_3_pairs\\pairs.pkl'
pickle_problems = 'f:\\paper\\i_4_problems\\problems.pkl'
# Maximum number of goals per problem.
k_max = 50
# Distance around the cells to generate the problems.
distance_rect = 5
# Maximum distance of the path between the goals.
distance_path_max = ((distance_rect*2) + 1)**2
# Number of tries to generate a problem (valid goals).
tries = 10

@log_2
def main(pickle_grids: str,
         pickle_pairs: str,
         pickle_problems: str,
         k_max: int,
         distance_rect: int,
         distance_path_max: int,
         tries: int) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """  
    grids = load_grids(pickle_grids)
    pairs = load_pairs(pickle_pairs)
    problems = gen_problems(grids=grids,
                            pairs=pairs,
                            k_max=k_max,
                            distance_rect=distance_rect,
                            distance_path_max=distance_path_max,
                            tries=tries)
    pickle_results(problems, pickle_problems)


main(pickle_grids,
     pickle_pairs,
     pickle_problems,
     k_max,
     distance_rect,
     distance_path_max,
     tries)
