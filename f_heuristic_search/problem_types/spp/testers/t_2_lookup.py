from f_heuristic_search.problem_types.spp.i_2_lookup import SPPLookup, Graph


def test_calc_h():
    graph = Graph.from_shape(rows=5)
    start = graph[0][0]
    goal = graph[4][4]
    lookup = {start: (goal, goal)}
    spp = SPPLookup(graph=graph, start=start, goal=goal, lookup=lookup)
    assert spp.calc_h(node=start) == 2
    assert spp.calc_h(node=goal) == 0
