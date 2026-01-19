from f_log.utils import set_debug, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.problems import ProblemOMSPPLite as ProblemLite
from f_search.ds.states import StateCell as State
from f_utils import u_pickle

Diamond = list[Cell]
PairDiamonds = tuple[Diamond, Diamond]
PairsDiamonds = list[PairDiamonds]


@log_2
def load_diamonds(pickle_diamonds: str) -> dict[str, list[Diamond]]:
    """
    ============================================================================
     Load the diamonds from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_diamonds)



@log_2
def get_problems(d_diamonds: dict[str, list[PairsDiamonds]]) -> list[ProblemLite]:
    """
    ========================================================================
     Get the problems for the given grids and diamonds.
    ========================================================================
    """
    problems: list[ProblemLite] = []
    for grid in d_diamonds:
        pairs_diamonds = d_diamonds[grid]
        problems_cur = _get_problems_from_grid(grid, pairs_diamonds)
        problems.extend(problems_cur)
    return problems

        
@log_2
def _get_problems_from_grid(grid: str,
                            pairs_diamonds: PairsDiamonds) -> list[ProblemLite]:
    """
    ========================================================================
     Get the problems for the given grid and pairs of diamonds.
    ========================================================================
    """
    problems: list[ProblemLite] = []
    for diamond_a, diamond_b in pairs_diamonds:
        for k in k_values:
            # Problem from diamond_a to diamond_b.
            # Start = first cell of diamond_a
            # Goals = first k cells of diamond_b.
            start = State(key=diamond_a[0])
            goals = [State(key=cell) for cell in diamond_b[:k]]
            problem = ProblemLite(grid=grid, start=start, goals=goals)
            problems.append(problem)
            # Problem from diamond_b to diamond_a.
            # Start = first cell of diamond_b
            # Goals = first k cells of diamond_a.
            start = State(key=diamond_b[0])
            goals = [State(key=cell) for cell in diamond_a[:k]]
            problem = ProblemLite(grid=grid, start=start, goals=goals)
            problems.append(problem)
    return problems

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
pickle_diamonds = 'f:\\paper\\i_2_diamonds\\diamonds.pkl'
pickle_problems = 'f:\\paper\\i_3_problems\\problems.pkl'

k_values = [10, 20, 30, 40, 50]


def main() -> None:
    d_diamonds = load_diamonds(pickle_diamonds)
    problems = get_problems(d_diamonds)
    pickle_results(problems, pickle_problems)


main()