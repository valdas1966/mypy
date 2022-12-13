from f_utils import u_tester
from f_abstract.loggable import Loggable


class TestLoggable:

    def __init__(self):
        u_tester.print_start(__file__)
        TestLoggable._tester_log()
        u_tester.print_finish(__file__)

    @staticmethod
    def _tester_log():
        class T(Loggable):
            def _log(self, **kwargs) -> None:
                self.kwargs = kwargs
        t = T()
        t._log(a=1)
        p0 = t.kwargs == {'a': 1}
        u_tester.run(p0)


if __name__ == '__main__':
    TestLoggable()
    print()
    print('Test Print:')
    t = Loggable()
    t._log(x=1, y=2)
    t._log(to_print=False, x=1, y=2)
    t._log(x=1, y=2, to_print=False)