from f_abstract.mixins.parentable import Parentable


def test_init():
    a = Parentable()
    b = Parentable(parent=a)
    assert a.parent is None
    assert b.parent == a
    assert not b.parent == b
    assert a.children == [b]


def test_parent():
    a = Parentable()
    b = Parentable()
    assert a.children == []
    assert b.parent is None
    b.parent = a
    assert a.children == [b]
    assert b.parent == a
    b.parent = None
    assert a.children == []
    assert b.parent is None
