from f_core.process_multi_threading import ProcessMulti
from f_core.process_tolerant import ProcessTolerant
from f_core.operation import Operation
import time
from random import randint


class Op(Operation):

    def _run(self) -> None:
        time.sleep(randint(1, 3))


class P(ProcessTolerant):

    def _set_ops(self) -> None:
        self._ops = [Op] * 3


class PM(ProcessMulti):

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        self._seconds_to_sleep = 1

    def _set_ops(self) -> None:
        self._ops = [P] * 5

    def _set_arg_ops(self) -> None:
        self._arg_ops = [{'id_session': i} for i in range(5)]


pm = PM()

