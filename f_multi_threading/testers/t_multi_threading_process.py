from f_utils import u_tester
from f_multi_threading.multi_threading_process import MultiThreadingProcess


class TestMultiThreadingProcess:

    def __init__(self):
        u_tester.print_start(__file__)
        TestMultiThreadingProcess.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        MultiThreadingProcess(kwargs={'f': print, 'params': ['a', 'b']})
        p0 = True
        u_tester.run(p0)


if __name__ == '__main__':
    TestMultiThreadingProcess()
