from f_core.operation import Operation
from f_core.process_tolerant import ProcessTolerant


class Op(Operation):
    pass


class P(ProcessTolerant):
    def _set_ops(self) -> None:
        self._ops = [Op]*3

p = P(a=1)



