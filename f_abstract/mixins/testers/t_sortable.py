from f_abstract.mixins.sortable import Sortable


class C(Sortable):

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def _key_comparison(self) -> list:
        return [self.a, self.b]


def test_multi_sort():
    x = C(1, 1)
    y = C(1, 2)
    assert x < y
