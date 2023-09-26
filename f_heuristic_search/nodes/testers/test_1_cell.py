from f_heuristic_search.nodes.node_1_cell import NodeCell


def test_str():
    node = NodeCell(name='Node', row=1, col=2)
    assert str(node) == 'Node(1,2)'
