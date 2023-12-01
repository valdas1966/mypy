from f_heuristic_search.algos.a_star import AStar
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_heuristic_search.problem_types.spp_grid import SPPGrid


grid = Grid(rows=4)
grid.make_invalid(cells=[(0, 2), (1, 2), (2, 2)])
start = grid[0][1]
goal = grid[0][3]
spp = SPPGrid(grid=grid, start=start, goal=goal)
astar = AStar(spp)
astar.run()
ordered_dict = dict.fromkeys(astar.closed)
for node in ordered_dict:
    print(node)

