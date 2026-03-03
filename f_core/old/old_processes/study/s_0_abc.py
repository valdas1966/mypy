from f_core.processes.i_0_base import ProcessBase


class Process(ProcessBase):

    def run(self) -> None:
        self._run_pre()
        self._run_post()


process = Process(verbose=True, name='Process ABC')
process.run()
print(process.time_start)
print(process.time_finish)
print(process.elapsed())
