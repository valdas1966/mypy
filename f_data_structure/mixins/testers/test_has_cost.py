from f_data_structure.mixins.has_cost import HasCost


class C(HasCost):

    def __init__(self, x: int):
        self.x = x

    def cost(self) -> int:
        return self.x


class MultiC(HasCost):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def cost(self) -> list[int]:
        return [self.x, self.y]


def test_cost():
    a = C(1)
    b = C(2)
    assert a.cost() == 1
    assert a == a
    assert a < b
    assert a <= b
    assert not a > b
    assert not a >= b


def test_multi():
    a = MultiC(1, 1)
    b = MultiC(1, 2)
    assert not a == b
    assert a < b
