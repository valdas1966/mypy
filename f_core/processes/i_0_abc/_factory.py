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
        class Stam(ProcessABC):
            def run(self) -> None:
                self._run_pre()
                self._run_post()
        return Stam(name='Stam', verbose=True)
