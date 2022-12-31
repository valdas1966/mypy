from f_abstract.inner.operation.a_2_dt import OperationDT
from f_utils import u_datetime as u_dt
from f_utils import u_dict


class OperationLog(OperationDT):
    """
    ============================================================================
     Description: Pre & Post Operation-Commands.
    ============================================================================
    """

    # OperationDT
    def _init_add_atts(self) -> None:
        """
        ========================================================================
         Description: Additional Attributes.
        ========================================================================
        """
        super()._init_add_atts()
        # bool : PreLogging or not
        self._to_pre_log = False
        # list : Attributes-Names that should not be logged
        self._black_list_log = ['black_list_log', 'to_pre_log', 'dt_start',
                                'dt_finish', 'title', 'e_msg', 'is_valid',
                                'verbose', 'logger_csv', 'Loggable__deli']

    def _add_black_list_log(self, li: list = list()) -> None:
        """
        ========================================================================
         Description: Extend Black-List of Log-Params.
        ========================================================================
        """
        self._black_list_log.extend(li)

    # OperationDT
    def _pre_run(self) -> None:
        """
        ========================================================================
         Description: Add Pre-Logging.
        ========================================================================
        """
        super()._pre_run()
        self._add_black_list_log()
        if self._to_pre_log:
            self._pre_log()

    # OperationDT
    def _post_run(self) -> None:
        """
        ========================================================================
         Description: Add Post-Logging.
        ========================================================================
        """
        super()._post_run()
        self._post_log()

    # Loggable
    def _pre_log(self) -> None:
        """
        ========================================================================
         Description: Pre-Logging.
        ========================================================================
        """
        params = {'state': 'START',
                  'status': None,
                  'dt_start': u_dt.to_str(self._dt_start),
                  'dt_finish': None,
                  'secs': None,
                  'title': self.title,
                  'e_msg': None,
                  'adds': self._additional_log_params()}
        self._log(**params)

    # Loggable
    def _post_log(self) -> None:
        """
        ========================================================================
         Description: Post-Logging.
        ========================================================================
        """
        secs = round((self._dt_finish - self._dt_start).total_seconds(), 2)
        params = {'state': 'FINISH',
                  'status': self.is_valid,
                  'dt_start': u_dt.to_str(self._dt_start),
                  'dt_finish': u_dt.to_str(self._dt_finish),
                  'secs': secs,
                  'title': self.title,
                  'e_msg': self.e_msg,
                  'adds': self._additional_log_params()}
        self._log(**params)

    def _additional_log_params(self) -> dict:
        """
        ========================================================================
         Description: Add Protected-Atts to the standard Operation-Log-Params.
        ========================================================================
        """
        d = self._get_log_atts()
        for key, val in d.items():
            if type(val) in (tuple, list, set, dict):
                d[key] = len(val)
            elif type(val) == str:
                d[key] = val[:100]
        return d

    def _get_log_atts(self) -> dict:
        """
        ========================================================================
         Desc: Return a dict of protected-atts, excluding those on blacklist.
        ========================================================================
        """
        d = self._get_protected_atts()
        d = u_dict.exclude_keys(d=d, keys_to_exclude=self._black_list_log)
        return d
