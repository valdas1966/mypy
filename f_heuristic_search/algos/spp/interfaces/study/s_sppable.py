from f_data_structure.cell import Cell
from f_data_structure.grid_cells import GridCells
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.algos.spp.interfaces.sppable import SPPAble


grid = GridCells(5)
start = Cell(1, 1, 's')
goal = Cell(3, 3, 'g')
spp = SPP(grid, start, goal)
a = SPPAble(spp)
print(a.name)