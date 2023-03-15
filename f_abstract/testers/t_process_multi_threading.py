from f_utils import u_tester
from f_abstract.process_multi_threading import ProcessMulti
from f_abstract.operation import Operation


class TestProcessMulti:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_process_multi()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_process_multi():
        class Op(Operation):
            def _run(self) -> None:
                print(self._i)
        class P(ProcessMulti):
            def _pre_run(self) -> None:
                self._seconds_to_sleep = 1
                super()._pre_run()
            def _set_ops(self) -> None:
                self._ops = [Op]*3
            def _set_arg_ops(self) -> None:
                self._arg_ops = [{'i': i} for i in [1, 2, 3]]
        P()
        p0 = True
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessMulti()
