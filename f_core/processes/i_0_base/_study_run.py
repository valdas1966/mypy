from f_core.processes.i_0_base import ProcessBase


class Process(ProcessBase):
    def _run(self) -> None:
        print('run')


p = Process()
p.run()
 