from f_utils import u_tester
from f_abstract.inner.process.a_3_ops import ProcessOps


class TestProcessOps:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_set_ops()
        self.__tester_set_arg_ops_empty()
        self.__tester_set_arg_ops_with_att()
        self.__tester_set_arg_ops_with_log_atts()
        self.__tester_set_arg_ops_with_custom_atts()
        self.__tester_proc_atts_not_logged()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_set_ops():
        class P(ProcessOps):
            def _set_ops(self) -> None:
                self._ops = [1]
        p = P(verbose=False)
        p0 = p._ops == [1]
        u_tester.run(p0)

    @staticmethod
    def __tester_set_arg_ops_empty():
        class P(ProcessOps):
            def _set_ops(self) -> None:
                self._ops = [1]
        p = P(verbose=False)
        p0 = p._arg_ops == [{'logger_csv': None}]
        u_tester.run(p0)

    @staticmethod
    def __tester_set_arg_ops_with_att():
        class P(ProcessOps):
            def _pre_run(self) -> None:
                self._verbose = False
                super()._pre_run()
            def _set_ops(self) -> None:
                self._ops = [1]
            def _set_arg_ops(self):
                self._arg_ops = [{'list': 1}]
        p = P()
        p0 = p._arg_ops == [{'list': 1, 'logger_csv': None}]
        u_tester.run(p0)

    @staticmethod
    def __tester_set_arg_ops_with_log_atts():
        class P(ProcessOps):
            def _pre_run(self) -> None:
                self._verbose = False
                super()._pre_run()
            def _set_ops(self) -> None:
                self._ops = [1,2]
        p = P(x=5)
        d = {'x': 5, 'logger_csv': None}
        p0 = p._arg_ops == [d, d]
        class P(ProcessOps):
            def _pre_run(self) -> None:
                self._verbose = False
                super()._pre_run()
            def _set_ops(self) -> None:
                self._ops = [1, 2]
            def _set_arg_ops(self):
                self._arg_ops = [{'list': 1}, {'b': 2}]
        p = P(x=5)
        p1 = p._arg_ops == [{'list': 1, 'x': 5, 'logger_csv': None},
                            {'b': 2, 'x': 5, 'logger_csv': None}]
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_set_arg_ops_with_custom_atts():
        class P(ProcessOps):
            def _pre_run(self) -> None:
                self._verbose = False
                super()._pre_run()
            def _set_ops(self) -> None:
                self._ops = [1, 2]
            def _add_to_arg_ops(self) -> None:
                arg_1 = 'f_1', None
                arg_2 = 'f_1', 'f_2'
                adds = [arg_1, arg_2]
                super()._add_to_arg_ops(adds=adds)
            def _f_1(self):
                pass
        p = P(x=5)
        p0 = p._arg_ops == [{'x': 5, 'f_1': p._f_1, 'f_2': p._f_1,
                             'logger_csv': None},
                            {'x': 5, 'f_1': p._f_1, 'f_2': p._f_1,
                             'logger_csv': None}]
        u_tester.run(p0)

    @staticmethod
    def __tester_proc_atts_not_logged():
        class P(ProcessOps):
            def _set_ops(self) -> None:
                self._ops = [1]
            def _add_black_list_log(self) -> None:
                super()._add_black_list_log(li=['x'])
            def _add_proc_atts_not_logged(self) -> None:
                super()._add_proc_atts_not_logged(s={'x'})
        p = P(verbose=False, x=2)
        p0 = p._proc_atts_not_logged == {'logger_csv', 'x'}
        u_tester.run(p0)


if __name__ == '__main__':
    TestProcessOps()
