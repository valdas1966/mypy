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
    __d_pre_log = dict()

    # dict : Post-Log Params
    __d_post_log = dict()

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
        kwargs_std = {'state': 'START', 'status': None,
                      'dt_start': u_dt.to_str(self._dt_start),
                      'dt_finish': None, 'secs': None, 'title': self.title,
                      'e_msg': None}
        self.__add_log_kwargs(d=self._d_pre_log)
        kwargs_std.update(self._d_pre_log)
        self._log(**kwargs_std)

    # Loggable
    def _post_log(self) -> None:
        """
        ========================================================================
         Description: Post-Logging.
        ========================================================================
        """
        secs = round((self._dt_finish - self._dt_start).total_seconds(), 2)
        kwargs_std = {'state': 'FINISH',
                      'status': self.is_valid,
                      'dt_start': u_dt.to_str(self._dt_start),
                      'dt_finish': u_dt.to_str(self._dt_finish),
                      'secs': secs,
                      'title': self.title,
                      'e_msg': self.e_msg}
        self.__add_log_kwargs(d=self._d_post_log)
        kwargs_std.update(self._d_post_log)
        super()._pre_log(**kwargs_std)

    def __add_log_kwargs(self, d: dict) -> None:
        """
        ========================================================================
         Description: Add [Pre|Post] Log-Kwargs.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. d : dict (pre_log_kwargs or post_log_kwargs).
        ========================================================================
        """
        for key, val in d:
            if val.startswith('self.'):
                att = val[5:]
                d[key] = self.__class__.__dict__[att]
            elif val.startswith('globs.'):
                att = val[6:]
                d[key] = self.__class__.__dict__['_globs'][att]
            else:
                d[key] = val
