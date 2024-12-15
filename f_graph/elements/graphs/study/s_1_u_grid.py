from f_graph.graphs.u_1_grid import UGraphGrid


graph = UGraphGrid.generate(rows=2, pct_valid=50)
start, goal = graph.sample(size=2)
print(bool(start), start)
print(bool(goal), goal)
print(graph.grid)
