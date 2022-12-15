"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. [With|Without] Pre-Logging.
    2. Pre and Post Logging.
    3. Logging-Collector by Inheritance.
================================================================================
"""

from f_abstract.inner.operation.a_3_log import OperationLog


class Op_1(OperationLog):
    pass


class Op_2(OperationLog):
    _to_pre_log = True


class Op_3(OperationLog):

    _to_pre_log = True

    def _add_pre_log(self) -> None:
        self._d_pre_log['a'] = 1

    def _add_post_log(self) -> None:
        self._d_post_log['a'] = 1


class A(OperationLog):
    def _add_post_log(self) -> None:
        self._d_post_log['a'] = 'A'


class B(A):
    def _add_post_log(self) -> None:
        super()._add_post_log()
        self._d_post_log['b'] = 'B'


Op_1()
Op_2()
Op_3()
B()
