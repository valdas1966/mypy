from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.graphs.i_0_mutable import GraphMutable as Graph
from f_data_structure.nodes.i_0_base import NodeBase as Node


def test_spp():
    start = Node(name='A')
    goal = Node(name='B')
    graph = Graph()
    graph.add_edge(node_a=start, node_b=goal)
    heuristics = {start: 100}
    spp = SPP(graph=graph, start=start, goal=goal, heuristics=heuristics)
    assert spp.heuristics(node=start) == 100
