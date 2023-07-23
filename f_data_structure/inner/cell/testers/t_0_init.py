from f_abstract.interfaces.nameable import Nameable
from f_abstract.interfaces.validatable import Validatable
from f_data_structure.xy import XY
from f_data_structure.cell import Cell


def test_init_default():
    cell = Cell(x=2, y=3)
    assert isinstance(cell, Nameable)
    assert isinstance(cell, XY)
    assert isinstance(cell, Validatable)
    assert cell.x == 2
    assert cell.y == 3
    assert cell.name is None
    assert cell.is_valid


def test_init_not_default():
    cell = Cell(x=1, y=2, name='MyCell', is_valid=False)
    assert isinstance(cell, Nameable)
    assert isinstance(cell, XY)
    assert isinstance(cell, Validatable)
    assert cell.x == 1
    assert cell.y == 2
    assert cell.name == "MyCell"
    assert not cell.is_valid


def test_str():
    cell = Cell(x=1, y=2, name='Cell')
    assert cell.__str__() == 'Cell(1,2)'
