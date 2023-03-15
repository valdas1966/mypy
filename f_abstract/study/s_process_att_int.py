from f_abstract.operation_io import OperationIO
from f_abstract.process_io import ProcessIO


class Op_1(OperationIO):

    def _run(self) -> None:
        self._x = 2
        self._output = {'x': self._x}


class Op_2(OperationIO):

    def _run(self) -> None:
        print(self._input['x'])
        self._output = self._input['x']


class P(ProcessIO):

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        self._x = 1
        self._output = self._x

    def _set_ops(self) -> None:
        self._ops = [Op_1, Op_2]



p = P()
