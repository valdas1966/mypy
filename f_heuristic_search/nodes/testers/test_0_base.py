from f_heuristic_search.nodes.node_0_base import NodeBase


def test_children():
    parent = NodeBase(name='Parent')
    child = NodeBase(name='Child', parent=parent)
    assert str(child.parent) == 'Parent'
