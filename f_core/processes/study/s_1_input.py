from f_core.processes.i_1_input import ProcessInput


class Process(ProcessInput[int]):

        def run(self) -> None:
            return print(self.input*2)


p = Process(_input=2)
p.run()
