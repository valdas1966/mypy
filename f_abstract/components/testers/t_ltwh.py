import pytest
from f_gui.components.ltwh import LTWH


@pytest.fixture
def ex_empty() -> LTWH:
    return LTWH()


@pytest.fixture
def ex_full() -> LTWH:
    return LTWH(10, 10, 80, 80)


def test_str(ex_empty, ex_full):
    assert str(ex_empty) == '(None, None, None, None)'
    assert str(ex_full) == '(10, 10, 80, 80)'

