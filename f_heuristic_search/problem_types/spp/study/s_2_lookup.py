from f_heuristic_search.problem_types.spp.i_2_lookup import SPPLookup, Graph


graph = Graph.from_shape(rows=5)
start = graph[0][0]
goal = graph[4][4]
lookup = {start: (goal, goal)}
spp = SPPLookup(graph=graph, start=start, goal=goal, lookup=lookup)
print(spp.calc_h(node=start))
print(spp.lookup_to_goal(node=start))
