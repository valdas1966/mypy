from f_core.processes.i_1_output.main import ProcessOutput


class Factory:
    """
    ============================================================================
     Factory for the ProcessOutput class.
    ============================================================================
    """

    @staticmethod
    def a() -> ProcessOutput[int]:
        """
        ========================================================================
         Create a ProcessOutput object with the output 'a'.
        ========================================================================
        """
        class A(ProcessOutput[int]):
            RECORD_SPEC = {'output': lambda o: o._output}
            def __init__(self):
                ProcessOutput.__init__(self, verbose=True, name='A')
            def _run(self) -> int:
                self._output = 1
        return A()
