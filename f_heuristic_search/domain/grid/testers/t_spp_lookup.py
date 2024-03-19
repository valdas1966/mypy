from f_heuristic_search.graphs.graph import Graph
from f_heuristic_search.domain.grid.spp_lookup import SPPLookup


def test_spp_lookup():
    graph = Graph(rows=3)
    start = graph[0][0]
    goal = graph[2][2]
    # The Manhattan-Distance shows Distance of 4 Nodes from Start to Goal
    # But the Lookup-Table shows 5 Nodes from Start to Goal
    lookup = {start: [start]*5}
    spp = SPPLookup(graph=graph, start=start, goal=goal, lookup=lookup)
    assert spp.heuristics(node=start) == 5
