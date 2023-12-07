from f_heuristic_search.problem_types.old_spp_grid import SPPGrid
from f_heuristic_search.domain.grid.node import NodeFCell
from f_data_structure.graphs.i_0_grid import GraphGrid
from f_data_structure.f_grid.grid_cells import GridCells
from f_data_structure.f_grid.cell import Cell


def test_grid():
    grid = GridCells(rows=2)
    start = Cell(0, 0)
    goal = Cell(1, 1)
    spp = SPPGrid(grid=grid, start=start, goal=goal)
    assert type(spp.graph) == type(GraphGrid)
    assert type(spp.start) == type(NodeFCell)
