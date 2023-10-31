from f_data_structure.nodes.node_0_nameable import NodeNameable as Node
from f_data_structure.graphs.graph_0_nodes import GraphNodes as Graph


def test_add_node():
    node = Node('node')
    graph = Graph()
    graph.add_node(node)
    assert graph.nodes() == [node]


def test_add_edge():
    node_a = Node('a')
    node_b = Node('b')
    graph = Graph()
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_edge(node_a, node_b)
    assert graph.neighbors(node_a) == [node_b]
