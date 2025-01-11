from f_ds.mixins.groupable import Groupable, Group
import pytest


class Items(Groupable):

    def __init__(self):
        self.items = [1, 2, 3]

    def to_group(self, name: str = None) -> Group:
        return Group(name=name, data=self.items)


def test_groupable():
    items = Items()
    assert len(items) == 3
    assert list(items) == [1, 2, 3]
    assert items.items == [x for x in items]
    assert bool(items)