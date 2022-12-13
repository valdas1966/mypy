from f_abstract.operation import Operation
from tenacity import retry, stop_after_attempt, wait_random_exponential
from datetime import datetime
from f_utils import u_datetime as u_dt


class Op(Operation):

    @retry(stop=stop_after_attempt(6),
           wait=wait_random_exponential(multiplier=1, max=10))
    def _run(self) -> None:
        print(u_dt.to_str(datetime.now()))
        1 / 0

Op()