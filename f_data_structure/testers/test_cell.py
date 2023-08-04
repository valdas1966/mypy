from f_abstract.interfaces.nameable import Nameable
from f_abstract.interfaces.validatable import Validatable
from f_data_structure.interfaces.xyable import XYAble
from f_data_structure.cell import Cell


def test_init_default():
    cell = Cell(x=2, y=3)
    assert cell.x == 2
    assert cell.y == 3
    assert cell.name is None


def test_init_not_default():
    cell = Cell(x=1, y=2, name='a')
    assert cell.x == 1
    assert cell.y == 2
    assert cell.name == 'a'


def test_traversable():
    cell = Cell(1, 2)
    assert cell.is_traversable
    cell.is_traversable = False
    assert not cell.is_traversable


def test_neighbors():
    cell = Cell(1, 2)
    north = Cell(1, 3)
    east = Cell(2, 2)
    south = Cell(1, 1)
    west = Cell(0, 2)
    expected = [north, east, south, west]
    assert cell.neighbors() == expected
