from f_heuristic_search.algos.spp.a_star_lookup import AStarLookup
from f_heuristic_search.problem_types.spp_lookup import SPPLookup
from f_data_structure.graphs.i_0_mutable import GraphMutable as Graph
from f_heuristic_search.nodes.i_2_f import NodeF as Node


def test_astar_manual():
    a = Node('A', w=1)
    b = Node('B', w=2)
    c = Node('C', w=1)
    d = Node('D', w=2)
    graph = Graph()
    graph.add_edge(a, b)
    graph.add_edge(a, c)
    graph.add_edge(b, d)
    graph.add_edge(c, d)
    heuristics = {a: 2, b: 1, c: 2, d: 0}
    lookup = {b: [d]}
    spp = SPPLookup(graph=graph,
                    start=a,
                    goal=d,
                    heuristics=heuristics,
                    lookup=lookup)
    astar = AStarLookup(spp=spp)
    astar.run()
    assert astar.optimal_path() == [a, c, d]
    assert astar.closed == {a, c, d}
    assert astar.open.items == [b]
