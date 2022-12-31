from f_abstract.operation import Operation
from f_abstract.process_tolerant import ProcessTolerant


class Op(Operation):
    pass


class P(ProcessTolerant):
    def _set_ops(self) -> None:
        self._ops = [Op]*3

p = P(a=1)



