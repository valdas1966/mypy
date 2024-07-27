from f_data_structure.graphs.i_1_grid import GraphGrid
from f_hs.nodes.i_3_f_cell import NodeFCell


g = GraphGrid.from_shape(rows=3, type_node=NodeFCell)
print(type(g[0][0]))
print(g)

g = GraphGrid.generate(rows=5, pct_non_valid=40)
print(g)
