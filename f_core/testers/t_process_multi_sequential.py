from f_utils import u_tester
from f_core.process_multi_sequential import ProcessMultiSequential
from f_core.process_io import ProcessIO
from f_core.operation_io import OperationIO


class TestProcessMultiSequential:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_multi_sequential()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_multi_sequential():
        class Op_1(OperationIO):
            def _run(self) -> None:
                self._output = self._input
        class Op_2(OperationIO):
            def _run(self) -> None:
                self._finished.append(self._input)
        class PSingle(ProcessIO):
            def _set_ops(self) -> None:
                self._ops = [Op_1, Op_2]
        class PMulti(ProcessMultiSequential):
            def _init_add_atts(self) -> None:
                super()._init_add_atts()
                self._finished = list()
        p = PMulti(process_single=PSingle, input=[1, 2, 3])
        p0 = p.finished = [1, 2, 3]
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessMultiSequential()
