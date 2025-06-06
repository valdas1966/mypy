from f_core.operation import Operation
from f_core.process_tolerant import ProcessTolerant
from f_core.process_tolerant_loop import ProcessLoop


class Op(Operation):
    pass


class PrTolerant(ProcessTolerant):

    def _set_ops(self) -> None:
        self._ops = [Op, Op]


class PrLoop(ProcessLoop):

    def _set_ops(self) -> None:
        self._ops = [PrTolerant]

PrLoop(secs_between_processes=2)
