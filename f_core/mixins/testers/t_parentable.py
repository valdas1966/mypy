from f_graph.nodes import HasParent


def test_path_from_root():
    a = HasParent()
    b = HasParent(parent=a)
    c = HasParent(parent=b)
    assert c.path_from_start() == [a, b, c]
