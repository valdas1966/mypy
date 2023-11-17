from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.graphs.i_2_grid import GraphGrid as Graph


def test():
    grid = Grid(2)
    graph = Graph(grid)
    node = graph.nodes()[0]
    neighbors = [graph.nodes()[1], graph.nodes()[2]]
    assert graph.neighbors(node) == neighbors