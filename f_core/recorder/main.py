
class Recorder:
    """
    ========================================================================
     Structured Event Recorder for Analysis.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, is_active: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._is_active: bool = is_active
        self._events: list[dict] = []

    @property
    def is_active(self) -> bool:
        """
        ====================================================================
         Return True if the Recorder is active.
        ====================================================================
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        """
        ====================================================================
         Set the Recorder's active state.
        ====================================================================
        """
        self._is_active = is_active

    @property
    def events(self) -> list[dict]:
        """
        ====================================================================
         Return the recorded Events.
        ====================================================================
        """
        return list(self._events)

    def record(self, event: dict) -> None:
        """
        ====================================================================
         Record an Event (no-op when inactive).
        ====================================================================
        """
        if self._is_active:
            self._events.append(event)

    def clear(self) -> None:
        """
        ====================================================================
         Clear all recorded Events.
        ====================================================================
        """
        self._events.clear()

    def to_dataframe(self):
        """
        ====================================================================
         Return Events as a pandas DataFrame.
        ====================================================================
        """
        import pandas as pd
        return pd.DataFrame(self._events)

    def __len__(self) -> int:
        """
        ====================================================================
         Return the number of recorded Events.
        ====================================================================
        """
        return len(self._events)

    def __bool__(self) -> bool:
        """
        ====================================================================
         Return True if the Recorder is active.
        ====================================================================
        """
        return self._is_active
