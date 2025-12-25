from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemSPP
from f_search.ds.states import StateCell as State
from f_ds.grids import GridMap as Grid
from f_ds.grids.cell import CellMap as Cell


def are_reachable(grid: Grid,
                  cell_start: Cell,
                  cell_goal: Cell) -> bool:
    """
    ========================================================================
     Check if the start and goal cells are reachable.
    ========================================================================
    """
    start = State(key=cell_start)
    goal = State(key=cell_goal)
    problem = ProblemSPP(grid=grid, start=start, goal=goal)
    solution = AStar(problem=problem).run()
    return bool(solution)
