from f_core.processes.i_1_input.main import ProcessInput


class Factory:
    """
    ============================================================================
     Factory for the ProcessInput class.
    ============================================================================
    """

    @staticmethod
    def a() -> ProcessInput:
        """
        ========================================================================
         Create a ProcessInput object with the input 'a'.
        ========================================================================
        """
        class A(ProcessInput):
            RECORD_SPEC = {'a': lambda o: o.a}
            def __init__(self, a: int):
                ProcessInput.__init__(self, a=a, verbose=True, name='A')
        return A(a=1)
