from f_utils import u_tester
from f_abstract.inittable import Initable


class TestInitible:

    def __init__(self):
        u_tester.print_start(__file__)
        TestInitible.__tester_init()
        TestInitible.__tester_add_kwargs()
        TestInitible.__tester_filter_kwargs()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        a = Initable(x=1)
        p0 = a.x == 1
        b = Initable(**{'y': 2})
        p1 = b.y == 2
        Initable()
        p2 = True
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_add_kwargs():
        class A(Initable):
            def _add_kwargs(self) -> None:
                self.y = 2
        a = A(x=1)
        p0 = (a.x == 1) and (a.y == 2)
        u_tester.run(p0)

    @staticmethod
    def __tester_filter_kwargs():
        a = Initable(a=1, b=2)
        kwargs = a._filter_kwargs(['b'])
        p0 = kwargs == {'b': 2}
        u_tester.run(p0)


if __name__ == '__main__':
    TestInitible()
