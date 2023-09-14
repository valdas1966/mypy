from f_heuristic_search.alias.grid import Grid
from f_heuristic_search.alias.cell import Cell
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.algos.spp.mixins.sppable import SPPAble


grid = Grid(5)
start = Cell(1, 1, 's')
goal = Cell(3, 3, 'g')
spp = SPP(grid, start, goal)
a = SPPAble(spp)
print(a.spp)
