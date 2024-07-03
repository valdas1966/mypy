from f_abstract.components.stats_items import StatsItems


def test_stats_items():
    c = ForTest(items=[1, 2, 3, 4])
    assert list(c.evens) == [2, 4]
    assert len(c.evens) == 2
    assert c.evens.pct() == 50
    assert str(c.evens) == 'Even Numbers([2, 4])'
    assert len(c.evens.sample(pct=50)) == 1


class ForTest:

    def __init__(self, items: list[int]) -> None:
        self._items = items
        self._evens = StatsItems[int](items=self.items,
                                      predicate=self.is_even,
                                      name='Even Numbers')

    @property
    def items(self) -> list[int]:
        return self._items

    @property
    def evens(self) -> StatsItems:
        return self._evens

    @staticmethod
    def is_even(item: int) -> bool:
        return item % 2 == 0
