from f_core.process_io import ProcessIO
from f_core.operation_io import OperationIO


class Op(OperationIO):

    def _run(self) -> None:
        if self._i == 2:
            raise Exception('Exception')
        print(self._i)


class P(ProcessIO):

    def _set_ops(self) -> None:
        self._ops = [Op] * 3

    def _set_arg_ops(self) -> None:
        self._arg_ops = [{'i': i} for i in [1, 2, 3]]


print(P().output)
