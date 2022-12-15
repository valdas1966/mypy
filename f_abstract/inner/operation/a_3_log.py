from f_abstract.inner.operation.a_2_dt import OperationDT
from f_utils import u_datetime as u_dt


class OperationLog(OperationDT):
    """
    ============================================================================
     Description: Pre & Post Operation-Commands.
    ============================================================================
    """

    # bool : PreLogging or not
    _to_pre_log = False

    # dict : Pre-Log Params
    _d_pre_log = dict()

    # dict : Post-Log Params
    _d_post_log = dict()

    # OperationDT
    def _pre_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Add Pre-Logging.
        ========================================================================
        """
        super()._pre_run(**kwargs)
        if self._to_pre_log:
            self._pre_log()

    # OperationDT
    def _post_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Add Post-Logging.
        ========================================================================
        """
        super()._post_run(**kwargs)
        self._post_log()

    # Loggable
    def _pre_log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Pre-Logging.
        ========================================================================
        """
        kwargs = {'state': 'START', 'status': None,
                      'dt_start': u_dt.to_str(self._dt_start),
                      'dt_finish': None, 'secs': None, 'title': self.title,
                      'e_msg': None}
        self._add_pre_log()
        kwargs.update(self._d_pre_log)
        self._log(**kwargs)

    # Loggable
    def _post_log(self) -> None:
        """
        ========================================================================
         Description: Post-Logging.
        ========================================================================
        """
        secs = round((self._dt_finish - self._dt_start).total_seconds(), 2)
        kwargs = {'state': 'FINISH',
                      'status': self.is_valid,
                      'dt_start': u_dt.to_str(self._dt_start),
                      'dt_finish': u_dt.to_str(self._dt_finish),
                      'secs': secs,
                      'title': self.title,
                      'e_msg': self.e_msg}
        self._add_post_log()
        kwargs.update(self._d_post_log)
        super()._pre_log(**kwargs)

    def _add_pre_log(self) -> None:
        """
        ========================================================================
         Description: Add Pre-Log Params into Params-Dict.
        ========================================================================
        """
        pass

    def _add_post_log(self) -> None:
        """
        ========================================================================
         Description: Add Post-Log Params into Params-Dict.
        ========================================================================
        """
        pass
