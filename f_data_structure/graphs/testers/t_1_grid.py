from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.f_grid.cell import Cell
from f_data_structure.graphs.i_1_grid import GraphGrid as Graph
from f_data_structure.nodes.i_2_cell import NodeCell
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell


def test_init_rows_cols():
    g = Graph(rows=5)
    assert g.shape() == '(5,5)'


def test_init_grid():
    grid = Grid(rows=5)
    graph = Graph(grid=grid)
    assert graph.shape() == '(5,5)'


def test_type_node():
    g = Graph(rows=5)
    assert g.type_node == NodeCell
    n = g[0][0]
    assert type(n) is NodeCell
    g = Graph(rows=5, type_node=NodeFCell)
    assert g.type_node == NodeFCell
    n = g[0][0]
    assert type(n) is NodeFCell


def test_get_neighbors():
    graph = Graph(rows=3)
    neighbors = graph.get_neighbors(graph[0][0])
    assert neighbors == [graph[0][1], graph[1][0]]


def test_generate():
    graph = Graph.generate(rows=5, pct_non_valid=20)



