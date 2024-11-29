from f_core.inner.operation.a_3_log import OperationLog


class OperationProcAtts(OperationLog):
    """
    ============================================================================
     Desc: Operation with Process-Attributes.
    ============================================================================
    """

    # OperationLog
    def _add_black_list_log(self) -> None:
        super()._add_black_list_log()
        self._black_list_log.append('proc_atts')

    # OperationLog
    def _collect_additional_log_params(self) -> dict:
        """
        ========================================================================
         Description: Add Process-Attributes to Operation-Log-Params.
        ========================================================================
        """
        d = super()._collect_additional_log_params()
        d.update(self.__get_proc_atts())
        return d

    def __get_proc_atts(self) -> dict:
        """
        ========================================================================
         Description: Return Process-Attributes of the Operation [_proc_atts].
        ========================================================================
        """
        d = self.__class__.__dict__
        if '_proc_atts' in d and type(d['_proc_atts']) == dict:
            return d['_proc_atts']
        return dict()
