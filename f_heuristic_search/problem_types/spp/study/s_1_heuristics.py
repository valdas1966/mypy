from f_heuristic_search.problem_types.spp.i_1_heuristics import \
    SPPHeuristics, Graph, Node


graph = Graph(rows=5)
start = graph[1][2]
goal = graph[3][2]
spp = SPPHeuristics(graph, start, goal, h_func='MANHATTAN_DISTANCE')
print(spp.calc_h(node=start))
