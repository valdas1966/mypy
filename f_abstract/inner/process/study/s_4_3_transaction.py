from f_abstract.inner.process.a_4_3_transaction import ProcessTransaction
from f_abstract.operation import Operation


class Op(Operation):

    def _run(self) -> None:
        if self._index == 1:
            raise Exception('index == 1')

    def _add_post_log(self) -> None:
        self._d_post_log['index'] = self._index


class Process(ProcessTransaction):

    _ops = [Op] * 3

    _arg_ops = [{'index': i} for i in range(3)]


p = Process()
