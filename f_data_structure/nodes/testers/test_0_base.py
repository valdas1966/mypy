from f_data_structure.nodes.node_0_hierarchy import NodeBase


def test_children():
    parent = NodeBase(name='Parent')
    child = NodeBase(name='Child', parent=parent)
    assert str(child.parent) == 'Parent'


def test_path_from():
    a = NodeBase('A')
    b = NodeBase('B', parent=a)
    c = NodeBase('C', parent=b)
    d = NodeBase('D', parent=b)
    assert a.path_from(a) == [a]
    assert a.path_from(c) == []
    assert b.path_from(b) == [b]
    assert b.path_from(a) == [a, b]
    assert c.path_from(a) == [a, b, c]
    assert d.path_from(c) == []
