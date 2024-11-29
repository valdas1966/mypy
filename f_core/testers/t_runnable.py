from f_utils import u_tester
from f_core.runnable import Runnable


class TestRunnable:

    def __init__(self):
        u_tester.print_start(__file__)
        TestRunnable.__tester_run()
        TestRunnable.__tester_pre_run()
        TestRunnable.__tester_post_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        class T(Runnable):
            def _run(self):
                self.x = 5
        t = T(x=2)
        p0 = t.x == 5
        u_tester.run(p0)

    @staticmethod
    def __tester_pre_run():
        class T(Runnable):
            def _pre_run(self):
                self.x = 5
            def _run(self):
                pass
        t = T(x=2)
        p0 = t.x == 5
        u_tester.run(p0)

    @staticmethod
    def __tester_post_run():
        class T(Runnable):
            def _post_run(self):
                self.x = 5

            def _run(self):
                self.x = 3

        t = T(x=2)
        p0 = t.x == 5
        u_tester.run(p0)


if __name__ == '__main__':
    TestRunnable()
