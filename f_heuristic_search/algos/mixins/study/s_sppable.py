from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.nodes.node_2_cell import NodeCell as Node
from f_heuristic_search.problem_types.spp_grid import SPP
from f_heuristic_search.algos.mixins.sppable import SPPAble


grid = Grid(5)
start = Node(1, 1, 's')
goal = Node(3, 3, 'g')
spp = SPP(grid, start, goal)
print(SPPAble(spp).spp)
