from f_heuristic_search.problem_types.kspp.old_i_1_heuristics import \
 KSPPHeuristics, Node
from f_data_structure.graphs.i_1_mutable import GraphMutable as Graph


def test_heuristics():
    def heuristics(node: Node, goals: tuple[Node, ...]) -> int:
        return 100
    node = Node(name='A')
    graph = Graph()
    graph.add_node(node=node)
    start = node
    goals = (node, node)
    kspp = KSPPHeuristics(graph=graph,
                          start=start,
                          goals=goals,
                          heuristics=heuristics)
    assert kspp.heuristics(node=start) == 100


