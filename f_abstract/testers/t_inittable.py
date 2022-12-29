from f_utils import u_tester
from f_abstract.inittable import Inittable


class TestInittible:

    def __init__(self):
        u_tester.print_start(__file__)
        TestInittible.__tester_init()
        TestInittible.__tester_add_attrs()
        TestInittible.__tester_filter_kwargs()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        a = Inittable(x=1)
        p0 = a._x == 1
        b = Inittable(**{'y': 2})
        p1 = b._y == 2
        Inittable()
        p2 = True
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_add_attrs():
        class A(Inittable):
            def _add_attrs(self) -> None:
                self._y = 2
        a = A(x=1)
        p0 = (a._x == 1) and (a._y == 2)
        u_tester.run(p0)

    @staticmethod
    def __tester_filter_kwargs():
        a = Inittable(a=1, b=2)
        kwargs = a._filter_kwargs(['_b'])
        p0 = kwargs == {'_b': 2}
        u_tester.run(p0)


if __name__ == '__main__':
    TestInittible()
