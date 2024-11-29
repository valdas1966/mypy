"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. [With|Without] Pre-Logging.
    2. Pre and Post Logging.
    3. Logging-Collector by Inheritance.
================================================================================
"""

from f_core.inner.operation.a_3_log import OperationLog


class Op_1(OperationLog):
    pass


class Op_2(OperationLog):
    _to_pre_log = True


class Op_3(OperationLog):
    _to_pre_log = True
    _a = 1


class Op_4(Op_3):
    _b = 2


print('Check: Only Post-Log')
Op_1()
print('Check: Pre & Post Log')
Op_2()
print('Check: Addition Log-Params (Protected-Attributes)')
Op_3()
print('Check: Inheritance')
Op_4()
