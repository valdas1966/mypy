from f_data_structure.cell import Cell
from f_data_structure.grid_cells import GridCells
from f_heuristic_search.problem_types.spp import SPP


def test_init():
    grid = GridCells(rows=5)
    start = Cell(1, 1)
    goal = Cell(2, 2)
    spp = SPP(grid, start, goal)
    assert spp.grid == grid
    assert spp.start == start
    assert spp.goal == goal
