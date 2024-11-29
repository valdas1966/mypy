from f_core.inner.process.a_3_ops import ProcessOps
from threading import Thread
import time


class ProcessMultiThreading(ProcessOps):

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        self._seconds_to_sleep = 0

    def _add_black_list_log(self, li: list = list()) -> None:
        li.append('seconds_to_sleep')
        super()._add_black_list_log(li=li)

    def _run(self) -> None:
        threads = list()
        for i, op in enumerate(self._ops):
            args = self._arg_ops[i]
            thread = Thread(target=op, kwargs=args)
            thread.start()
            time.sleep(self._seconds_to_sleep)
            threads.append(thread)
        for thread in threads:
            thread.join()
