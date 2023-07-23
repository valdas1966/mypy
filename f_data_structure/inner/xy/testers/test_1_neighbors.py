from f_data_structure.inner.xy.i_1_neighbors import XYNeighbors


def test_neighbors():
    xy = XYNeighbors(x=1, y=2)
    north = XYNeighbors(x=1, y=3)
    east = XYNeighbors(x=2, y=2)
    south = XYNeighbors(x=1, y=1)
    west = XYNeighbors(x=0, y=2)
    expected = [north, east, south, west]
    assert xy.neighbors() == expected


def test_neighbor_north():
    xy = XYNeighbors(x=1, y=2)
    expected = XYNeighbors(x=1, y=3)
    assert xy.neighbor_north() == expected


def test_neighbor_south():
    xy = XYNeighbors(x=1, y=2)
    expected = XYNeighbors(x=1, y=1)
    assert xy.neighbor_south() == expected


def test_neighbor_west():
    xy = XYNeighbors(x=1, y=2)
    expected = XYNeighbors(x=0, y=2)
    assert xy.neighbor_west() == expected


def test_neighbor_east():
    xy = XYNeighbors(x=1, y=2)
    expected = XYNeighbors(x=2, y=2)
    assert xy.neighbor_east() == expected
