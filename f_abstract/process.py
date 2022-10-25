from abc import ABC, abstractmethod
from f_abstract.inittable import Inittable


class Process(ABC, Inittable):

    # str: Title of the Process
    _title = None

    # Result of the Process
    _res = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._log_start()
        self._run()
        self._log_finish()

    def res(self) -> any:
        """
        ========================================================================
         Description: Return the Process' Result.
        ========================================================================
        """
        return self._res

    @abstractmethod
    def _run(self) -> None:
        """
        ========================================================================
         Description: Run a Process.
        ========================================================================
        """
        pass

    def _log(self, **params) -> None:
        """
        ========================================================================
         Description: Log an Operation.
        ========================================================================
        """
        pass

    def _log_start(self) -> None:
        """
        ========================================================================
         Description: Log the Process' Start.
        ========================================================================
        """
        self._log(status='SUCC', state='START', title=self._title)

    def _log_finish(self) -> None:
        """
        ========================================================================
         Description: Log the Process' Finish.
        ========================================================================
        """
        self._log(status='SUCC', state='FINISH', title=self._title)
