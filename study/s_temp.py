from f_core.inner.operation.a_2_dt import OperationDT
from f_utils import u_datetime as u_dt
import inspect

from f_core.inner.operation.a_1_init import OperationInit
from f_core.inittable import Inittable
from datetime import datetime





class OperationLog(OperationDT):
    """
    ============================================================================
     Description: Pre & Post Operation-Commands.
    ============================================================================
    """

    # bool : PreLogging or not
    _to_pre_log = False

    def get_protected_atts(self):
        def is_protected_att(name: str, value: object) -> tuple:
            base_value = getattr(self.__class__.__base__, name, None)
            if name.startswith('_'):
                if not name.startswith('__'):
                    if not callable(value):
                        if base_value is None or value is not base_value:
                            return (name, value)
            return None
        atts = inspect.getmembers(self.__class__)
        return dict(
            att for att in (is_protected_att(name, value) for name, value in atts)
            if att is not None)


class C(OperationLog):
    _c = 3


c = C()
print(c.get_protected_atts())
