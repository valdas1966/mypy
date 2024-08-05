from f_abstract.operation import Operation
from f_utils import u_tester


class TestOperation:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_operation()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_operation():
        class Op(Operation):
            """
            ============================================================================
             Description: Test-Operation.
            ============================================================================
             Attributes:
            ----------------------------------------------------------------------------
                1. list : int
                2. b : int
                3. c : int
            ============================================================================
            """
            def _pre_run(self) -> None:
                self._a = 1
                super()._pre_run()
            def _run(self) -> None:
                self._b = 2
            def _post_run(self) -> None:
                self._c = 3
                super()._post_run()
        op = Op(a=None, b=None, c=None)
        p0 = op._a, op._b, op._c == 1, 2, 3
        u_tester.run(p0)


if __name__ == '__main__':
    TestOperation()
