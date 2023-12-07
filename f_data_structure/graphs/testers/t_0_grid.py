from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.f_grid.cell import Cell
from f_data_structure.graphs.i_0_grid import GraphGrid as Graph
from f_data_structure.nodes.i_2_cell import NodeCell


def test_getitem():
    graph = Graph(rows=3)
    assert type(graph[0][0]) == NodeCell


def test_gen_neighbors():
    graph = Graph(rows=3)
    neighbors = graph.get_neighbors(graph[0][0])
    assert neighbors == [graph[0][1], graph[1][0]]


