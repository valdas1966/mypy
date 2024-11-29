import pytest
from f_core.mixins.validatable_public import ValidatablePublic


@pytest.fixture
def ex_valid() -> ValidatablePublic:
    return ValidatablePublic()

@pytest.fixture
def ex_invalid() -> ValidatablePublic:
    return ValidatablePublic(is_valid=False)


def test_init(ex_valid, ex_invalid):
    assert ex_valid
    assert not ex_invalid

def test_set(ex_valid, ex_invalid):
    ex_valid.set_invalid()
    ex_invalid.set_valid()
    assert not ex_valid
    assert ex_invalid
