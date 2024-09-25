from f_abstract.mixins.cursorable import Cursorable


def test_list():
    c = Cursorable(data=[1, 2, 3])
    assert list(c) == [1, 2, 3]
