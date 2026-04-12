from f_core.mixins.has import HasName
from f_core.recorder import Recorder
from time import time, perf_counter_ns


class ProcessBase(HasName):
    """
    ============================================================================
     ABC of Process-Classes.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 name: str = 'ProcessABC',
                 is_recording: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        # Recorder
        self._recorder: Recorder = Recorder(is_active=is_recording)
        # Init Time Attributes
        self._elapsed: float | None = None
        self._time_start: float | None = None
        self._time_finish: float | None = None
        # Lap timer (seconds since previous call)
        self._time_lap_prev: float | None = None

    @property
    def elapsed(self) -> float:
        return self._elapsed

    @property
    def recorder(self) -> Recorder:
        """
        ========================================================================
         Return the Process's Recorder.
        ========================================================================
        """
        return self._recorder

    def seconds_since_last_call(self) -> float:
        """
        ========================================================================
         Return seconds elapsed since the previous call to this method.
        ========================================================================
        """
        now = time()
        if self._time_lap_prev is None:
            self._time_lap_prev = now
            return 0
        delta = now - self._time_lap_prev
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
        self._time_start = time()
        self._event_prev_ns = perf_counter_ns()

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
        self._elapsed = self._time_finish - self._time_start

    def _record_event(self, **kwargs) -> None:
        """
        ========================================================================
         Record an Event with Duration (nanoseconds).
        ========================================================================
        """
        if self._recorder:
            now = perf_counter_ns()
            kwargs['duration'] = now - self._event_prev_ns
            self._event_prev_ns = now
            self._enrich_event(kwargs)
            self._recorder.record(kwargs)

    def _enrich_event(self, event: dict) -> None:
        """
        ========================================================================
         Enrich Event with Subclass-Specific Details.
        ========================================================================
        """
        pass
