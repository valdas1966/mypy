from f_data_structure.graphs.graph_1_hierarchy import GraphHierarchy as Graph
from f_data_structure.nodes.node_1_hierarchical import NodeHierarchical as Node


def test_children():
    graph = Graph()
    a = Node('a')
    b = Node('b', parent=a)
