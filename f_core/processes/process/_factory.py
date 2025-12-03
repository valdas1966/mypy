from f_core.processes.process.main import Process
from f_core.mixins.has.record import HasRecord


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
            def __init__(self, input: int):
                Process.__init__(self, input=input, verbose=True, name='Square')
            def _run(self) -> None:
                self._output = self._input * self._input
        return Square

    @staticmethod
    def with_record() -> type[Process]:
        class A(HasRecord):
            RECORD_SPEC = {'a': lambda o: bool(True)}
        class WithRecord(Process[None, A]):
            def __init__(self, name='WithRecord') -> None:
                Process.__init__(self, name=name, verbose=True)
            def _run(self) -> None:
                self._output = A()
        return WithRecord
