from f_utils import u_tester
from f_core.loggable import Loggable


class TestLoggable:

    def __init__(self):
        u_tester.print_start(__file__)
        TestLoggable.__tester_log()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_log():
        class T(Loggable):
            def _log(self, **kwargs) -> None:
                self.kwargs = kwargs
        t = T()
        t._log(a=1)
        p0 = t.kwargs == {'list': 1}
        u_tester.run(p0)


if __name__ == '__main__':
    TestLoggable()
