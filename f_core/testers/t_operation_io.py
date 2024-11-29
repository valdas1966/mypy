from f_utils import u_tester
from f_core.operation_io import OperationIO


class TestOperationIO:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_operation_io()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_operation_io():
        class Op(OperationIO):
            def _run(self) -> None:
                self._output = self._input * 2
        op = Op(input=3)
        p0 = op.output == 6
        u_tester.run(p0)


if __name__ == '__main__':
    TestOperationIO()
