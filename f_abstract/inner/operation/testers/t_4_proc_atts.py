from f_utils import u_tester
from f_abstract.inner.operation.temp import OperationProcAtts


class TestOperationProcAtts:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_proc_atts()
        self.__tester_not_in_log_params()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_proc_atts():
        proc_atts = {'a': 1, 'b': 2}
        op = OperationProcAtts(proc_atts=proc_atts)
        p0 = op._proc_atts['a'] = 1
        p1 = op._proc_atts['b'] = 2
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_not_in_log_params():
        proc_atts = {'a': 1}
        op = OperationProcAtts(proc_atts=proc_atts)
        p0 = 'proc_atts' not in op._additional_log_params()
        u_tester.run(p0)


if __name__ == '__main__':
    TestOperationProcAtts()
