from f_utils import u_tester
from f_abstract.validdable import Validdable


class TestValiddable():

    def __init__(self):
        u_tester.print_start(__file__)
        TestValiddable._tester_is_valid()
        u_tester.print_finish(__file__)


    @staticmethod
    def _tester_is_valid():
        class T(Validdable):
            def turn_on(self):
                self._is_valid = True
            def turn_off(self):
                self._is_valid = False
        t = T()
        p0 = t.is_valid is None
        t.turn_on()
        p1 = t.is_valid is True
        t.turn_off()
        p2 = t.is_valid is False
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestValiddable()
