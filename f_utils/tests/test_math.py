from f_utils import u_math


def test_max_permutations() -> None:
    values = [1, 2, 3]
    result = u_math.max_permutations(values, 2)
    expected = 6
    assert result == expected
