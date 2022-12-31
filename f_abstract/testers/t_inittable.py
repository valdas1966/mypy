from f_utils import u_tester
from f_abstract.inittable import Inittable


class TestInittible:

    def __init__(self):
        u_tester.print_start(__file__)
        TestInittible.__tester_init()
        TestInittible.__tester_init_add_atts()
        self.__tester_init_run_funcs()
        self.__tester_get_protected_atts()
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
    def __tester_init_add_atts():
        class A(Inittable):
            def _init_add_atts(self) -> None:
                self._y = 2
        a = A(x=1)
        p0 = (a._x == 1) and (a._y == 2)
        u_tester.run(p0)

    @staticmethod
    def __tester_init_run_funcs():
        class A(Inittable):
            def _init_run_funcs(self) -> None:
                self._increment()
            def _increment(self):
                self._x += 1
        a = A(x=1)
        p0 = a._x == 2
        u_tester.run(p0)

    @staticmethod
    def __tester_get_protected_atts():
        class A(Inittable):
            def _init_add_atts(self) -> None:
                self._a = 1
        class B(A):
            pass
        t = B(b=2)
        p0 = t._get_protected_atts() == {'a': 1, 'b': 2}
        u_tester.run(p0)


if __name__ == '__main__':
    TestInittible()
