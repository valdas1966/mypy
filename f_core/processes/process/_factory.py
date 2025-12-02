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
            def _run(self) -> None:
                self._output = self._input * self._input
        return Square
