from f_utils import u_tester
from f_abstract.process_io import ProcessIO
from f_abstract.operation_io import OperationIO


class TestProcessIO:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_process_io()
        self.__tester_process_io_when_op_fails()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_process_io():
        class Op(OperationIO):
            def _run(self) -> None:
                self._output = self.input * 2
        class P(ProcessIO):
            def _set_ops(self) -> None:
                self._ops = [Op] * 3
        p = P(input=1)
        p0 = p.output == 8
        u_tester.run(p0)

    @staticmethod
    def __tester_process_io_when_op_fails():
        class Op(OperationIO):
            def _run(self) -> None:
                if self.input == 2:
                    raise Exception('ERR MSG')
                self._output = self.input * 2
        class P(ProcessIO):
            def _set_ops(self) -> None:
                self._ops = [Op] * 3
        p = P(input=1)
        p0 = p.output is None
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessIO()
