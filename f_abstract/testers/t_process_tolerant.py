from f_utils import u_tester
from f_abstract.process_tolerant import ProcessTolerant
from f_abstract.operation import Operation


class TestProcessTolerant:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_process_tolerant()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_process_tolerant():
        class Op(Operation):
            """
            ====================================================================
             Description: Test Operation.
            ====================================================================
             Attributes:
            --------------------------------------------------------------------
                1. i : int
                2. to_fail : bool
            ====================================================================
            """
            def _run(self) -> None:
                if self._to_fail:
                    raise Exception('ERR MSG')
                else:
                    self._f(i=self._i)
        class Process(ProcessTolerant):
            def _set_ops(self) -> None:
                self._ops = [Op] * 3
            def _set_arg_ops(self):
                self._arg_ops = [{'i': 1, 'to_fail': False},
                                 {'i': 2, 'to_fail': True},
                                 {'i': 3, 'to_fail': False}]
            def _add_to_arg_ops(self) -> None:
                super()._add_to_arg_ops(adds=[('f', None)])
            def _f(self, i: int) -> None:
                self._li.append(i)
        p = Process(li=list())
        p0 = p._li == [1, 3]
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessTolerant()
