from f_abstract.mixins.nameable import Nameable


def test_init_default():
    nameable = Nameable()
    assert nameable.name is None


def test_init_not_default():
    nameable = Nameable("John")
    assert nameable.name == "John"


def test_set():
    nameable = Nameable("John")
    nameable.name = "Jane"
    assert nameable.name == "Jane"


def test_eq():
    a = Nameable('test')
    b = Nameable('test')
    assert a == b


def test_str():
    a = Nameable('test')
    assert str(a) == 'test'


def test_repr():
    a = Nameable('test')
    assert a.__repr__() == '<Nameable: test>'
    class B(Nameable):
        pass
    b = B(name='SubClass')
    assert b.__repr__() == '<B: SubClass>'
