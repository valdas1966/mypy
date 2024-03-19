from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete, \
    Graph


graph = Graph(rows=5)
start = graph[1][2]
goal = graph[2][3]
spp = SPPConcrete(graph=graph, start=start, goal=goal)
print(spp)
