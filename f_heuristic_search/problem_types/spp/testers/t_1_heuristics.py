from f_heuristic_search.problem_types.spp.i_1_heuristics import \
    SPPHeuristics, Graph


def test_heuristics():
    graph = Graph(rows=5)
    start = graph[1][3]
    goal = graph[3][3]
    spp = SPPHeuristics(graph, start, goal)
    assert spp.calc_h(node=start) == 2
