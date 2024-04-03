from f_heuristic_search.algos.spp.i_1_astar import AStar, NodeFCell
from f_heuristic_search.problem_types.spp.i_1_heuristics import \
    (SPPHeuristics, GraphGrid as Graph)


graph = Graph.from_shape(rows=3, type_node=NodeFCell)
start = graph[0][0]
goal = graph[2][2]
spp = SPPHeuristics(graph=graph, start=start, goal=goal)
astar = AStar(spp=spp)
print(astar.is_path_found)
astar.run()
print(astar.is_path_found)
print(astar.optimal_path())
