from f_abstract.inner.operation.a_2_dt import OperationDT
import time


class Op(OperationDT):
    def _run(self) -> None:
        time.sleep(1)


operator = Op()
print(operator._dt_start)
print(operator._dt_finish)
