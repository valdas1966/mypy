from f_core.processes.i_2_io.main import ProcessIO


class Factory:
    """
    ============================================================================
     Factory for the ProcessIO class.
    ============================================================================
    """

    @staticmethod
    def square() -> type[ProcessIO[int, int]]:
        """
        ========================================================================
         Create a ProcessIO object that squares the input.
        ========================================================================
        """
        class Square(ProcessIO[int, int]):
            RECORD_SPEC = {'input': lambda o: o.input,
                           'output': lambda o: o._output}
            def __init__(self, name='Square', verbose=True, input=input) -> None:
                ProcessIO.__init__(self, name=name, verbose=verbose, input=input)
            def _run(self) -> None:
                self._output = self.input * self.input
        return Square
