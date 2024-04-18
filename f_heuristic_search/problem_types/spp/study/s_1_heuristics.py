from f_heuristic_search.problem_types.spp.old_i_1_heuristics import \
    SPPHeuristics, Graph


graph = Graph.from_shape(rows=5)
start = graph[1][2]
goal = graph[3][2]
spp = SPPHeuristics(graph, start, goal,
                    h_func=SPPHeuristics.Heuristic.MANHATTAN_DISTANCE)
print(spp.calc_h(node=start))
