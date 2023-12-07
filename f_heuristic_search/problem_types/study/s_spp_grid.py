from f_heuristic_search.problem_types.old_spp_grid import SPPGrid as SPP
from f_data_structure.graphs.i_0_grid import GraphGrid as Graph
from f_data_structure.f_grid.grid_cells import GridCells as Grid


grid = Grid(rows=2)
start = grid[0][0]
goal = grid[1][1]
spp = SPP(grid=grid, start=start, goal=goal)
print(type(spp.start))
