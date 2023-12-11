from f_heuristic_search.algos.spp.a_star.i_1_manual import AStarManual
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
    heuristics = {a: 2, b: 1, c: 1, d: 1, e: 0}
    spp = SPP(graph=graph, start=a, goal=e, heuristics=heuristics)
    astar = AStarManual(spp=spp)
    astar.run()
    assert astar.optimal_path() == [a, c, e]
    assert astar.closed == {a, b, c, e}
    assert astar.open.items == [d]
