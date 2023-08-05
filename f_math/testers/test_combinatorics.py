from f_math import u_combinatorics


def test_cartesian_product():
    prod = u_combinatorics.cartesian_product(2, 3)
    expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert prod == expected
