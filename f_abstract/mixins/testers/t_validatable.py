import pytest
from f_abstract.mixins.validatable import Validatable


@pytest.fixture
def ex_valid() -> Validatable:
    return Validatable()

@pytest.fixture
def ex_invalid() -> Validatable:
    return Validatable(is_valid=False)


def test_init(ex_valid, ex_invalid):
    assert ex_valid
    assert not ex_invalid

def test_set(ex_valid, ex_invalid):
    ex_valid.set_invalid()
    ex_invalid.set_valid()
    assert not ex_valid
    assert ex_invalid
