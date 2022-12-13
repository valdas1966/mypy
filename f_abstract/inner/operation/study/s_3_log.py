"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. [With|Without] Pre-Logging.
    2. Pre and Post Logging.
================================================================================
"""

from f_abstract.inner.operation.a_3_log import OperationLog


class Op_1(OperationLog):
    pass


class Op_2(OperationLog):
    _to_pre_log = True


class Op_3(OperationLog):

    _to_pre_log = True

    def _add_pre_log_kwargs(self) -> None:
        self._pre_log_kwargs['a'] = 1

    def _add_post_log_kwargs(self) -> None:
        self._post_log_kwargs['a'] = 1


class Op_4(OperationLog):

    _to_pre_log = True

    _d_pre_log['x'] = 1


Op_1()
Op_2()
Op_3()
