from f_abstract.interfaces.nameable import Nameable


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



