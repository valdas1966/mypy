from f_core.processes.process.main import Process


class Factory:
    """
    ============================================================================
     Factory for the Process class.
    ============================================================================
    """

    @staticmethod
    def Square() -> type[Process[int, int]]:
        """
        ========================================================================
         Create a Process object that squares the input.
        ========================================================================
        """
        class Square(Process[int, int]):
            RECORD_SPEC = {'input': lambda o: o._input,
                           'output': lambda o: o._output}
            def __init__(self, input: int):
                Process.__init__(self, input=input, verbose=True, name='Square')
            def _run_pre(self) -> None:
                self._str_start += f' [Input={self._input}]'
                super()._run_pre()
            def _run(self) -> None:
                self._output = self._input * self._input
            def _run_post(self) -> None:
                self._str_finish += f' [Output={self._output}]'
                super()._run_post()
        return Square
