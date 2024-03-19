from f_data_structure.graphs.i_0_grid import GraphGrid
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell


class G(GraphGrid):
    def __init__(self, rows: int):
        GraphGrid.__init__(self,  rows=rows, type_node=NodeFCell)

g = G(rows=5)
print(g.shape())
a = g[0][0]
print(a)
print(type(a))
