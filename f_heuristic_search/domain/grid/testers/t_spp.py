from f_heuristic_search.graphs.grid import Graph
from f_heuristic_search.domain.grid.spp import SPP


def test_spp():
    graph = Graph(rows=3)
    start = graph[0][0]
    goal = graph[2][2]
    spp = SPP(graph=graph, start=start, goal=goal)
    assert spp.heuristics(node=start) == 4
