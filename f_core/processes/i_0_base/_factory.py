from f_core.processes.i_0_base.main import ProcessBase


class Factory:
    """
    ============================================================================
     Factory for ProcessABC objects.
    ============================================================================
    """

    @staticmethod
    def nested() -> ProcessBase:
        """
        ========================================================================
         Create a ProcessABC object with the name 'Nested'.
        ========================================================================
        """
        class Nested(ProcessBase):
            def __init__(self) -> None:
                ProcessBase.__init__(self, name='Nested')
            def _run(self) -> None:
                proc_1 = ProcessBase(name='Nested | Inner 1')
                proc_1.run()
                proc_2 = ProcessBase(name='Nested | Inner 2')
                proc_2.run()
        return Nested()
