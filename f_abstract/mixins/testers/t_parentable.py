from f_abstract.mixins.parentable import Parentable


def test_path_from_root():
    a = Parentable()
    b = Parentable(parent=a)
    c = Parentable(parent=b)
    assert c.path_from_root() == [a, b, c]
