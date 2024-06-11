import pytest
from f_ds.grids.cell import Cell


@pytest.fixture
def ex_00() -> Cell:
    return Cell(is_valid=False)

@pytest.fixture
def ex_23() -> Cell:
    return Cell(2, 3)


def test_init(ex_00, ex_23):
    assert not ex_00
    assert ex_23
