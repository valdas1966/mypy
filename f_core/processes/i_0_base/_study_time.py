from f_core.processes.i_0_base import ProcessBase
import time


class Process(ProcessBase):

    def _run(self) -> None:
        print(self.seconds_since_last_call())
        time.sleep(1)
        print(self.seconds_since_last_call())
        time.sleep(2)
        print(self.seconds_since_last_call())
        time.sleep(3)
        print(self.seconds_since_last_call())
        self._run_post()


process = Process(name='Process ABC')
process.run()
print(process.elapsed)
