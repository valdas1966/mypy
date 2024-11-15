from f_abstract.processes.i_1_output import ProcessOutput


class Process(ProcessOutput[int]):

    def run(self) -> int:
        return 2


p = Process()
output = p.run()
print(output)
