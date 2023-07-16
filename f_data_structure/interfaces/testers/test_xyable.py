from f_data_structure.interfaces.xyable import XYAble


def test_init():
    xy = XYAble(x=1, y=2)
    assert xy.x == 1
    assert xy.y == 2


def test_distance():
    xy_1 = XYAble(x=1, y=2)
    xy_2 = XYAble(x=2, y=4)
    assert xy_1.distance(xy_2) == 3


def test_str():
    xy = XYAble(x=1, y=2)
    assert str(xy) == '(1,2)'


def test_eq():
    xy_1 = XYAble(x=1, y=1)
    xy_2 = XYAble(x=1, y=1)
    xy_3 = XYAble(x=3, y=3)
    assert xy_1 == xy_2
    assert not xy_1 == xy_3


def test_neighbors():
    xy = XYAble(x=1, y=2)
    north = XYAble(x=1, y=3)
    east = XYAble(x=2, y=2)
    south = XYAble(x=1, y=1)
    west = XYAble(x=0, y=2)
    expected = [north, east, south, west]
    assert xy.neighbors() == expected


def test_neighbor_north():
    xy = XYAble(x=1, y=2)
    expected = XYAble(x=1, y=3)
    assert xy.neighbor_north() == expected


def test_neighbor_south():
    xy = XYAble(x=1, y=2)
    expected = XYAble(x=1, y=1)
    assert xy.neighbor_south() == expected


def test_neighbor_west():
    xy = XYAble(x=1, y=2)
    expected = XYAble(x=0, y=2)
    assert xy.neighbor_west() == expected


def test_neighbor_east():
    xy = XYAble(x=1, y=2)
    expected = XYAble(x=2, y=2)
    assert xy.neighbor_east() == expected
