from f_data_structure.nodes.i_1_path import NodePath as Node


def test_path_to_root():
    a = Node(name='A')
    assert a.path_from_root() == [a]
    b = Node(name='B', parent=a)
    c = Node(name='C', parent=b)
    assert c.path_from_root() == [a, b, c]
