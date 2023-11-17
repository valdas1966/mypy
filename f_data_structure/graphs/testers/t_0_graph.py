from f_data_structure.graphs.i_0_graph import Graph
from f_data_structure.nodes.i_0_node import Node


def test_graph():
    a = Node('A')
    b = Node('B')
    c = Node('C')
    g = Graph()
    assert g.nodes() == []
    g.add_edge(a, b)
    g.add_edge(a, c)
    assert g.nodes() == [a, b, c]
    assert g.neighbors(a) == [b, c]
    d = Node('D')
    g.add_node(d)
    assert g.nodes() == [a, b, c, d]
    assert g.neighbors(d) == []


def test_type_node():
    g = Graph()
    node = g.type_node('N')
    assert node.__str__() == 'N'
