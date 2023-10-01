from f_data_structure.nodes.node_1_cell import NodeCell as Node
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_heuristic_search.problem_types.spp import SPP


def test_str():
    grid = Grid(rows=5, name='TEST')
    start = Node(1, 1)
    goal = Node(2, 2)
    spp = SPP(grid, start, goal)
    assert spp.grid == grid
    assert spp.start == start
    assert spp.goal == goal
    assert str(spp) == f'SPP[TEST(5,5)]: START(1,1) -> GOAL(2,2)'


def test_generate():
    spp = None
    while not spp:
        spp = SPP.generate(rows=5, name='TEST', pct_non_valid=40)
    assert spp.grid.name.startswith('TEST')
    assert spp.start.name.startswith('START')
    assert spp.goal.name.startswith('GOAL')
