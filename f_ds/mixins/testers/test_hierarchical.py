from f_data_structure.mixins.hierarchical import Hierarchical


def test_add_child():
    a = Hierarchical()
    b = Hierarchical(parent=a)
    c = Hierarchical()
    a.add_child(c)
    assert a.children == [b, c]


def test_remove_child():
    a = Hierarchical()
    b = Hierarchical(parent=a)
    a.remove_child(b)
    assert a.children == []


def test_set_new_parent():
    a = Hierarchical()
    b = Hierarchical(parent=a)
    c = Hierarchical()
    b.parent = c
    assert a.children == []
    assert c.children == [b]


def test_path_from_ancestor():
    a = Hierarchical(name='A')
    b = Hierarchical(name='B', parent=a)
    c = Hierarchical(name='C', parent=b)
    assert c.path_from_ancestor(a) == [a, b, c]
    assert c.path_from_ancestor(c) == [c]
    assert b.path_from_ancestor(c) is None
