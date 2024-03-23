from f_heuristic_search.problem_types.spp_lookup import SPPLookup
from f_data_structure.graphs.i_1_mutable import GraphMutable as Graph
from f_data_structure.nodes.i_0_base import NodeBase as Node


def test_spp_lookup():
    start = Node(name='START')
    goal = Node(name='GOAL')
    heuristics = {start: 100}
    lookup = {start: [start]}
    graph = Graph()
    graph.add_edge(node_a=start, node_b=goal)
    spp = SPPLookup(graph, start, goal, heuristics, lookup)
    assert spp.heuristics(node=start) == 1
