from f_abstract.process_tolerant import ProcessTolerant
from f_abstract.operation import Operation


class Op(Operation):

    def _run(self) -> None:
        self._f(1)


class P(ProcessTolerant):

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        self._li = list()

    def _f(self, n: int) -> None:
        self._li.append(n)

    def _set_ops(self) -> None:
        self._ops = [Op, Op]

    def _add_proc_atts_not_logged(self, s: set = set()) -> None:
        super()._add_proc_atts_not_logged(s={'f'})

    #def _set_arg_ops(self) -> None:
    #    self._arg_ops = [{'f': self._f}, {'f': self._f}]

    def _post_run(self) -> None:
        super()._post_run()
        print(self._li)


P()
