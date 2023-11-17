from f_data_structure.graphs.i_1_path import GraphPath as Graph
from f_data_structure.nodes.i_1_path import NodePath as Node


def test_neighbors():
    a = Node(name='A')
    b = Node(name='B', parent=a)
    c = Node(name='C', parent=b)
    g = Graph()
    g.add_edge(a, b)
    g.add_edge(b, c)
    assert g.neighbors(b) == [c]
