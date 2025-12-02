from f_core.processes.i_1_input.main import ProcessInput


class Factory:
    """
    ============================================================================
     Factory for the ProcessInput class.
    ============================================================================
    """

    @staticmethod
    def a() -> type[ProcessInput]:
        """
        ========================================================================
         Create a ProcessInput object with the input 'a'.
        ========================================================================
        """
        class A(ProcessInput[int]):
            RECORD_SPEC = {'input': lambda o: o.input}
            def __init__(self, input: int):
                ProcessInput.__init__(self, input=input, verbose=True, name='A')
        return A
