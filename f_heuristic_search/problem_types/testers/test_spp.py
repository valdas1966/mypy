from f_heuristic_search.alias.grid import Grid
from f_heuristic_search.alias.cell import Cell
from f_heuristic_search.problem_types.spp import SPP


def test_str():
    grid = Grid(num_rows=5, name='Test')
    start = Cell(1, 1)
    goal = Cell(2, 2)
    spp = SPP(grid, start, goal)
    assert spp.grid == grid
    assert spp.start == start
    assert spp.goal == goal
    assert str(spp) == f'SPP[Test(5,5)]: START(1,1) -> GOAL(2,2)'


def test_generate():
    spp = None
    while not spp:
        spp = SPP.generate(5, name='Test', pct_non_traversable=40)
    assert spp.grid.name.startswith('Test')
    assert spp.start.name.startswith('START')
    assert spp.goal.name.startswith('GOAL')

