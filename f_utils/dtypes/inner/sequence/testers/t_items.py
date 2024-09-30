from f_utils.dtypes.inner.sequence.items import Items


def is_lower(s: str) -> bool:
    return s.islower()


def test_filter() -> None:
    assert Items[str].filter(seq='Abc', predicate=is_lower) == 'bc'


def test_sample() -> None:
    assert len(Items.sample(seq='abcd', pct=50)) == 2
