from f_utils.dtypes.inner.sequence.indexes import Indexes


def is_lower(s: str) -> bool:
    return s.islower()


def test_filter() -> None:
    assert Indexes.filter('Abc', predicate=is_lower) == [1, 2]


def test_sample() -> None:
    assert len(Indexes.sample(seq='abcd', pct=50)) == 2
