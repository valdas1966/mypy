from f_data_structure.f_tree.node import Node


def test_name():
    a = Node(name='A')
    assert str(a) == 'A'


def test_parent():
    a = Node('A')
    b = Node('B', parent=a)
    assert a == b.parent
    assert list(a.children) == [b]
