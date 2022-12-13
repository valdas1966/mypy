from f_abstract.inner.operation.a_1_init import OperationInit
from datetime import datetime


class OperationDT(OperationInit):
    """
    ============================================================================
     Description: Pre & Post Operation DateTimes.
    ============================================================================
    """

    # datetime : Operation Start-Time
    _dt_start = None

    # datetime : Operation Finish-Time
    _dt_finish = None

    # Runnable
    def _pre_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Set Operation DateTime-Start.
        ========================================================================
        """
        self._dt_start = datetime.now()
        super()._pre_run(**kwargs)

    # Runnable
    def _post_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Set Operation Finish-Time.
        ========================================================================
        """
        self._dt_finish = datetime.now()
        super()._post_run(**kwargs)
