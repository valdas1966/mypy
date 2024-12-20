from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.u_1_grid import UGraphGrid
from f_graph.algos.i_1_bfs import BFS
from f_hs.algos.one_to_one.a_star_grid import AStarGrid, NodeFCell


graph = UGraphGrid.gen(rows=100, pct_valid=75, type_node=NodeFCell)
start, goal = graph.sample(size=2)
problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
bfs = BFS(problem=problem)
astar = AStarGrid(problem=problem)
print(bfs.path.get() == astar.path.get())


