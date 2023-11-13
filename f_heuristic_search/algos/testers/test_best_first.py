from f_heuristic_search.algos.a_star import BestFirst
from f_data_structure.nodes.node_3_f import NodeF as Node
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_heuristic_search.problem_types.spp_grid import SPP


def test_run():
    grid = Grid(4)
    grid[0][2].is_valid = False
    grid[1][2].is_valid = False
    start = Node(0, 0)
    goal = Node(0, 3)
    spp = SPP(grid, start, goal)
    bf = BestFirst(spp)
    bf.run()
    assert list(bf.closed.keys()) == [Node(0, 0), Node(0, 1), Node(1, 1),
                                      Node(1, 0), Node(2, 1), Node(2, 2),
                                      Node(2, 3), Node(1, 3), Node(0, 3)]



