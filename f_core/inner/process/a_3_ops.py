from f_core.inner.process.a_1_init import ProcessInit
from f_utils import u_dict


class ProcessOps(ProcessInit):
    """
    ============================================================================
     Description: List of Operations and List of their Arguments (dicts).
    ============================================================================
    """

    # OperationLog
    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        # list[Operation] : List of Operations to Execute
        self._ops = None
        # list[dict] : List of Operations-Arguments
        self._arg_ops = None
        # set : Procedure-Attributes that are not being logged
        self._proc_atts_not_logged = {'loguru', 'stack_driver'}

    def _add_proc_atts_not_logged(self, s: set = set()) -> None:
        """
        ========================================================================
         Desc: Add Names of Procedure-Attributes that are not being logged.
        ========================================================================
        """
        self._proc_atts_not_logged = set.union(self._proc_atts_not_logged, s)

    # OperationLog
    def _add_black_list_log(self, li: list = None) -> None:
        li_new = ['ops', 'arg_ops', 'proc_atts_not_logged']
        if li:
            li_new.extend(li)
        super()._add_black_list_log(li=li_new)

    # ProcessInit
    def _pre_run(self) -> None:
        self._add_proc_atts_not_logged()
        super()._pre_run()
        self._set_ops()
        self._set_arg_ops()
        self._add_to_arg_ops()

    def _set_ops(self) -> None:
        """
        ========================================================================
         Desc: Set the list of operations to run.
        ========================================================================
        """
        pass

    def _set_arg_ops(self) -> None:
        """
        ========================================================================
         Desc: Set the list of arguments for each Operation.
        ========================================================================
        """
        self._arg_ops = [{}] * len(self._ops)

    def _add_to_arg_ops(self, adds: list[tuple] = list()) -> None:
        """
        ========================================================================
         Desc: Add arguments for each Operation.
        ========================================================================
        """
        d_adds = dict()
        for name, name_new in adds:
            if name_new:
                d_adds[name_new] = getattr(self, f'_{name}')
            else:
                d_adds[name] = getattr(self, f'_{name}')
        for i, args in enumerate(self._arg_ops):
            args = u_dict.union(args, self._get_log_atts())
            args = u_dict.union(args, self._get_proc_atts_not_logged())
            args = u_dict.union(args, d_adds)
            self._arg_ops[i] = args

    def _get_proc_atts_not_logged(self) -> dict:
        """
        ========================================================================
         Desc: Return Procedure-Attributes that are not being logged.
        ========================================================================
        """
        d = {att: getattr(self, f'_{att}') for att in self._proc_atts_not_logged}
        return d
