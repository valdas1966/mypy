from f_abstract.interfaces.validatable import Validatable


def test_init_default():
    obj = Validatable()
    assert obj.is_valid


def test_init_not_default():
    obj = Validatable(is_valid=False)
    assert not obj.is_valid


def test_set():
    obj = Validatable(is_valid=True)
    obj.is_valid = False
    assert not obj.is_valid
