from f_data_structure.inner.xy.i_1_distance import XYDistance


def test_distance():
    xy_1 = XYDistance(x=1, y=2)
    xy_2 = XYDistance(x=2, y=4)
    assert xy_1.distance(xy_1) == 0
    assert xy_1.distance(xy_2) == 3
