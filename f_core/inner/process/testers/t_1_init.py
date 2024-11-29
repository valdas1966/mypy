from f_utils import u_tester
from f_core.inner.process.a_1_init import ProcessInit


class TestProcessInit:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_process_init()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_process_init():
        p = ProcessInit()
        p0 = p._to_pre_log
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessInit()
