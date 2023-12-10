from f_heuristic_search.algos.spp.a_star.manual import AStarManual
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.algos.spp.node import Node
from f_data_structure.graphs.i_0_mutable import GraphMutable as Graph


def test_astar_manual():
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    e = Node('E')
    graph = Graph()
    graph.add_edge(a, b)
    graph.add_edge(a, c)
    graph.add_edge(b, d)
    graph.add_edge(d, e)
    graph.add_edge(c, e)
    heuristics = {a: 1, b: 0, c: 1, d: 0, e: 0}
    spp = SPP(graph=graph, start=a, goal=d, heuristics=heuristics)
    astar = AStarManual(spp=spp)
    astar.run()
    assert astar.optimal_path() == [a, c, d]
