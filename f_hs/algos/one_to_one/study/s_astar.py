from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_grid import GraphGrid, Grid
from f_hs.heuristics.i_1_manhattan import HeuristicsManhattan
from f_hs.nodes.i_1_f_cell import NodeFCell
from f_hs.algos.one_to_one.a_star import AStar


grid = Grid(3)
graph = GraphGrid(grid=grid, type_node=NodeFCell)
start = graph[0, 0]
goal = graph[2, 2]
problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
heuristics = HeuristicsManhattan(problem=problem)
astar = AStar(problem=problem, heuristics=heuristics.eval)



