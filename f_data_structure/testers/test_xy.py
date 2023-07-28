from f_data_structure.xy import XY
from f_utils.u_enum import XYDistanceMetric


def test_init_default():
    xy = XY(x=1, y=2)
    assert xy.x == 1
    assert xy.y == 2
    assert xy.name is None


def test_init_not_default():
    xy = XY(name='a', x=1, y=2)
    assert xy.x == 1
    assert xy.y == 2
    assert xy.name == 'a'


def test_distance():
    xy_1 = XY(x=1, y=2)
    xy_2 = XY(x=1.5, y=2)
    assert xy_1.distance(xy_2) == 0.5
    assert xy_1.distance(other=xy_2, metric=XYDistanceMetric.MANHATTAN) == 0.5
