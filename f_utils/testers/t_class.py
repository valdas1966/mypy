from f_utils import u_tester
from f_utils import u_class


class TestClass:

    def __init__(self):
        u_tester.print_start(__file__)
        TestClass.__tester_get_protected_attributes()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_get_protected_attributes():
        class A:
            v_1 = 1
            _v_2 = 2
            __v_3 = 3
        class B(A):
            v_4 = 4
            _v_5 = 5
            __v_6 = 6
            def _f(self):
                pass
        b = B()
        atts_test = u_class.get_protected_atts(self=b)
        atts_true = {'_v_2': 2, '_v_5': 5}
        p0 = atts_test == atts_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestClass()
