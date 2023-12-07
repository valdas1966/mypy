from f_heuristic_search.nodes.i_2_f import NodeF as Node
from f_data_structure.graphs.i_0_mutable import GraphMutable as Graph


def test_run():
    graph = Graph()
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    graph.add_edge(a, b)
    graph.add_edge(a, c)
    graph.add_edge(b, d)
    graph.add_edge(c, d)