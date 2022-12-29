from f_utils import u_tester
from f_abstract.inner.process.a_2_init_io import ProcessInitIO


class TestProcessInitIO:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_process_init_io()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_process_init_io():
        class Process(ProcessInitIO):
            def _run(self) -> None:
                self._output = self._input * 2
        p = Process(input=1)
        p0 = p._to_pre_log
        p1 = p.input == 1
        p2 = p.output == 2
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestProcessInitIO()
