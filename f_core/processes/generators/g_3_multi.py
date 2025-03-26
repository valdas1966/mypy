from f_core.processes.i_3_multi import ProcessMulti, DataInput
from f_core.processes.i_1_input import ProcessInput


class GenProcessMulti:

    @staticmethod
    def print_multi() -> ProcessMulti:
        
        class ProcessPrint(ProcessInput):
            """
            ============================================================================
             Process that prints the input.
            ============================================================================
            """
            def run(self) -> None:
                self._run_pre()
                print(self.name, self.input)
                self._run_post()

        process = ProcessPrint
        inputs = [str(i+1) for i in range(5)]
        threads = 2
        data = DataInput(process=process, inputs=inputs, threads=threads)
        return ProcessMulti[ProcessPrint](name='Print Multi', _input=data)


p = GenProcessMulti.print_multi()
p.run()
