from f_utils import u_tester
from f_core.inner.operation.a_3_log import OperationLog


class TestOperationLog:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_log_int()
        self.__tester_log_list()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_log_int():
        op = OperationLog(x=5)
        p0 = op._additional_log_params()['x'] == 5
        u_tester.run(p0)


    @staticmethod
    def __tester_log_list():
        op = OperationLog(li=[1, 2, 3])
        p0 = op._additional_log_params()['li'] == 3
        u_tester.run(p0)


if __name__ == '__main__':
    TestOperationLog()
