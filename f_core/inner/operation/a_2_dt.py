from f_core.inner.operation.a_1_init import OperationInit
from datetime import datetime


class OperationDT(OperationInit):
    """
    ============================================================================
     Description: Pre & Post Operation DateTimes.
    ============================================================================
    """

    # Inittable
    def _init_add_atts(self) -> None:
        """
        ========================================================================
         Description: Additional Attributes.
        ========================================================================
        """
        super()._init_add_atts()
        # datetime : Operation Start-Time
        self._dt_start = None
        # datetime : Operation Finish-Time
        self._dt_finish = None

    # Runnable
    def _pre_run(self) -> None:
        """
        ========================================================================
         Description: Set Operation DateTime-Start.
        ========================================================================
        """
        self._dt_start = datetime.now()
        super()._pre_run()

    # Runnable
    def _post_run(self) -> None:
        """
        ========================================================================
         Description: Set Operation Finish-Time.
        ========================================================================
        """
        self._dt_finish = datetime.now()
        super()._post_run()
