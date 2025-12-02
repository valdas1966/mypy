from f_core.processes.i_0_abc.main import ProcessABC


class Factory:
    """
    ============================================================================
     Factory for ProcessABC objects.
    ============================================================================
    """

    @staticmethod
    def stam() -> ProcessABC:
        """
        ========================================================================
         Create a ProcessABC object with the name 'Stam'.
        ========================================================================
        """
        return ProcessABC(name='Stam', verbose=True)

    @staticmethod
    def nested() -> ProcessABC:
        """
        ========================================================================
         Create a ProcessABC object with the name 'Nested'.
        ========================================================================
        """
        class Nested(ProcessABC):
            def _run(self) -> None:
                ProcessABC(name='Nested | Inner 1', verbose=True)
                ProcessABC(name='Nested | Inner 2', verbose=True)
        return Nested(name='Nested', verbose=True)
