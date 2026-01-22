from f_core.processes.i_0_abc.main import ProcessABC


class Factory:
    """
    ============================================================================
     Factory for ProcessABC objects.
    ============================================================================
    """

    @staticmethod
    def nested() -> ProcessABC:
        """
        ========================================================================
         Create a ProcessABC object with the name 'Nested'.
        ========================================================================
        """
        class Nested(ProcessABC):
            def __init__(self) -> None:
                ProcessABC.__init__(self, name='Nested')
            def _run(self) -> None:
                proc_1 = ProcessABC(name='Nested | Inner 1')
                proc_1.run()
                proc_2 = ProcessABC(name='Nested | Inner 2')
                proc_2.run()
        return Nested()
