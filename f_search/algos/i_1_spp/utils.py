from f_search.algos.i_1_spp import AStar, Dijkstra
from f_search.problems import ProblemSPP
from f_search.ds.states import StateCell as State
from f_ds.grids import GridMap as Grid
from f_ds.grids.cell import CellMap as Cell
import random


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

def len_path(grid: Grid,
             start: Cell,
             goal: Cell) -> int:
    """
    ========================================================================
     Return the length of the path from the start to the goal.
    ========================================================================
    """
    start = State(key=start)
    goal = State(key=goal)
    problem = ProblemSPP(grid=grid, start=start, goal=goal)
    solution = AStar(problem=problem).run()
    return len(solution.path)


def are_within_distance(grid: Grid,
                        cells: list[Cell],
                        distance: int) -> bool:
    """
    ========================================================================
     Check if the cells are within a given distance.
    ========================================================================
    """
    cell_a = cells[0]
    cells_b = cells[1:]
    for cell_b in cells_b:
        path = len_path(grid=grid, start=cell_a, goal=cell_b)
        if path > distance:
            return False 
    return True


def random_cells_up_to_distance(grid: Grid,
                                cells: list[Cell],
                                distance: int,
                                k: int,
                                tries: int) -> list[Cell]:
    """
    ========================================================================
     Return the cells up to a given distance.
    ========================================================================
    """    
    for i in range(tries):
        print(f'Try={i+1}')
        cells_random = random.sample(population=cells, k=k)
        if are_within_distance(grid=grid,
                               cells=cells_random,
                               distance=distance):
            return cells_random
    return None


def k_neighborhood(grid: Grid,
                   cell: Cell,
                   k: int) -> list[Cell]:
    """
    ========================================================================
     Return the k-neighborhood of a cell.
    ========================================================================
    """
    cell_goal = Cell.Factory.Million()
    goal = State(key=cell_goal)
    start = State(key=cell)
    problem = ProblemSPP(grid=grid, start=cell, goal=goal)
    solution = AStar(problem=problem).run()
    return solution.path
