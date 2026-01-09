from f_core.mixins.validatable import Validatable
from f_core.mixins.has import HasName
from time import time


class ProcessABC(HasName, Validatable):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self, name: str = 'ProcessABC') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        Validatable.__init__(self)
        # Init Time Attributes
        self._elapsed: int = None
        self._time_start: float = None
        self._time_finish: float = None
        
        # Lap timer (seconds since previous call)
        self._time_lap_prev: int | None = None

    def seconds_since_last_call(self) -> int:
        """
        ========================================================================
         Return seconds elapsed since the previous call to this method.
        ========================================================================
        """
        now = time()
        if self._time_lap_prev is None:
            self._time_lap_prev = now
            return 0
        delta = int(now - self._time_lap_prev)
        self._time_lap_prev = now
        return delta

    def run(self) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        self._run_pre()
        self._run()
        self._run_post()

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run necessary operations before the start of the Process.
        ========================================================================
        """
        self._elapsed = None
        self._time_start: float = time()

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
        self._elapsed = int(self._time_finish - self._time_start)
