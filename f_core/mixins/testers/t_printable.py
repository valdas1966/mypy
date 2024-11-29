import pytest
from f_core.mixins.printable import Printable


@pytest.fixture
def ex() -> Printable:
    class Sub(Printable):
        def __str__(self) -> str:
            return 'Test'
    return Sub()


def test_str(ex):
    assert str(ex) == 'Test'


def test_repr(ex):
    assert repr(ex) == '<Sub: Test>'
