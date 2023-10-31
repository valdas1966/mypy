from f_data_structure.mixins.has_cost import HasCost


class C(HasCost):

    def __init__(self, x: int):
        self.x = x

    def cost(self) -> int:
        return self.x


def test_cost():
    a = C(1)
    b = C(2)
    assert a.cost() == 1
    assert a == a
    assert a < b
    assert a <= b
    assert not a > b
    assert not a >= b
