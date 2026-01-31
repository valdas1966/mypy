from f_core.processes.i_0_abc import ProcessABC


class Process(ProcessABC):
    def _run(self) -> None:
        print('run')


p = Process()
p.run()
 