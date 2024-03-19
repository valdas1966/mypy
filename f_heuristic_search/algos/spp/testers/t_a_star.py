from f_heuristic_search.algos.spp.a_star import AStar
from f_heuristic_search.problem_types.spp.i_0_concrete import SPP
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
    spp = SPP(graph=graph, start=a, goal=d, heuristics=heuristics)
    astar = AStar(spp=spp)
    astar.run()
    assert astar.optimal_path() == [a, c, d]
    assert astar.closed == {a, b, c, d}
    assert astar.open.items == []
