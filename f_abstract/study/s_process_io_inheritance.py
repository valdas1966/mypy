from f_abstract.operation_io import OperationIO
from f_abstract.process_io import ProcessIO
from f_abstract.process_tolerant import ProcessTolerant


class Op(OperationIO):

    def _run(self) -> None:
        print(self.input)


class PIO(ProcessIO):

    def _set_ops(self) -> None:
        self._ops = [Op]


class P(ProcessTolerant):

    def _set_ops(self) -> None:
        self._ops = [PIO]

    def _set_arg_ops(self) -> None:
        self._arg_ops = [{'_input': 2}]


p = P(input=1)
