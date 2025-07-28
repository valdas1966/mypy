from f_graph.graphs.i_1_grid import GraphGrid, Grid


grid = Grid(2)
print(grid)

grid[0][0].set_invalid()
print(grid)

graph = GraphGrid(grid=grid)
print(graph)

print(graph.nodes())