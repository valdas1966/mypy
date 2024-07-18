import pytest
from f_abstract.components.ltwh import LTWH


@pytest.fixture
def ex() -> LTWH:
    return LTWH(10, 10, 80, 80)


def test_width(ex):
    assert ex.width == 70


def test_height(ex):
    assert ex.height == 70
