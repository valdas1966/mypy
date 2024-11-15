from f_abstract.processes.i_2_io import ProcessIO


class Process(ProcessIO[int, int]):

    def run(self) -> int:
        return self.input * 2


p = Process(_input=2)
output = p.run()
print(output)
