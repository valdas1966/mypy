import heapq
from f_data_structure.interfaces.xyorderable import XYOrderable
from f_data_structure.cell import Cell
from f_heuristic_search.nodes.node_f import NodeF

xy_1 = XYOrderable(1, 1)
xy_2 = XYOrderable(2, 2)

cell_1 = Cell(1, 1)
cell_2 = Cell(2, 2)

node_1 = NodeF(1, 1)
node_1._g, node_1._h = 1, 10
node_2 = NodeF(2, 2)
node_2._g, node_2._h = 2, 10

open = list()

heapq.heappush(open, node_1)
heapq.heappush(open, node_2)

node_1._g = 3
heapq.heapify(open)

print(heapq.heappop(open))

