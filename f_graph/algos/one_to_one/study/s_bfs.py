from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_grid import GraphGrid, Grid, NodePathCell
from f_graph.algos.one_to_one.i_1_bfs import BFS


grid = Grid(3)
graph = GraphGrid(grid=grid, type_node=NodePathCell)
start = graph[0, 0]
goal = graph[2, 2]
problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
bfs = BFS(problem)


