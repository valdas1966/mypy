from f_utils import u_random


def test_groups() -> None:
    values = [1, 2, 3]
    groups = u_random.to_groups(values, n=5, k=2)
    assert len(groups) == 5
    assert len(groups.pop()) == 2
