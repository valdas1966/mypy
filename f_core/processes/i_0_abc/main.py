from f_core.mixins.has.record import HasRecord
from f_core.mixins.validatable import Validatable
from f_core.mixins.verbosable import Verbosable
from time import time


class ProcessABC(HasRecord, Verbosable, Validatable):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    # Record Specification
    RECORD_SPEC = {'elapsed': lambda o: o.elapsed}

    # Factory
    Factory = None

    def __init__(self,
                 verbose: bool = False,
                 name: str = 'Process') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRecord.__init__(self, name=name)
        Verbosable.__init__(self, verbose=verbose, name=name)
        Validatable.__init__(self)
        # Init Time Attributes
        self._elapsed: int = None
        self._time_start: float = None
        self._time_finish: float = None
        self._str_start: str = '[Start]'
        self._str_finish: str = '[Finish]'
        self._run_pre()
        self._run()
        self._run_post()

    @property
    def time_start(self) -> float:
        """
        ========================================================================
         Return the start time of the process running.
        ========================================================================
        """
        return self._time_start

    @property
    def time_finish(self) -> float:
        """
        ========================================================================
         Return the finish time of the process running.
        ========================================================================
        """
        return self._time_finish

    def elapsed(self) -> int:
        """
        ========================================================================
         Return the elapsed time of the process running (in milliseconds).
        ========================================================================
        """
        return self._elapsed

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run necessary operations before the start of the Process.
        ========================================================================
        """
        self._elapsed = None
        self._time_start: float = time()
        self.print(msg=self._str_start)

    def _run(self) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        pass

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the Process finishes.
        ========================================================================
        """
        self._time_finish = time()
        self._elapsed = int((self._time_finish - self._time_start) * 1000)  # Convert to milliseconds
        self._str_finish += f' [Elapsed={self._elapsed}]'
        self.print(msg=self._str_finish)
