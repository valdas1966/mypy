from f_core.old_processes import ProcessSequence, DataSequence
from f_core.processes.i_1_input import ProcessInput


class GenProcessSequence:

    @staticmethod
    def print_sequence() -> ProcessSequence:

        class ProcessPrint(ProcessInput[str]):

            def run(self) -> None:
                self._run_pre()
                print(self.name, self._input)
                self._run_post()

        process = ProcessPrint
        inputs = [str(i+1) for i in range(5)]
        data = DataSequence[ProcessPrint, str](process=process, inputs=inputs)
        return ProcessSequence(_input=data)


p = GenProcessSequence.print_sequence()
p.run()

