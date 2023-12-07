from f_heuristic_search.algos.spp.a_star import AStar
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.domain.grid.node import NodeFCell
from f_data_structure.graphs.i_0_grid import GraphGrid as Graph


graph = Graph(rows=4, type_node=NodeFCell)
graph.make_invalid([(0, 2), (1, 2), (2, 2)])
start = graph[0][1]
goal = graph[0][3]
spp = SPP(graph, start, goal)
astar = AStar(spp)
astar.run()
