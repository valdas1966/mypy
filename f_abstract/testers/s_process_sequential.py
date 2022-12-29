from f_abstract.process_sequential import ProcessSequential
from f_abstract.operation import Operation


class Op(Operation):

    def _run(self) -> None:
        if self._index == 1:
            raise Exception('index == 1')


class Process(ProcessSequential):

    _ops = [Op] * 3

    _arg_ops = [{'index': i} for i in range(10)]


p = Process()
