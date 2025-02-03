from f_core.components.enum_callable import EnumCallable
from typing import Type


class GenEnumCallable:
    """
    ============================================================================
     Generator of EnumCallable.
    ============================================================================
    """

    class A:
        def __init__(self):
            self.name = 'A'

    class B(A):
        def __init__(self):
            self.name = 'B'

    class C(A):
        def __init__(self):
            self.name = 'C'

    @staticmethod
    def gen_a() -> Type[EnumCallable]:
        """
        ========================================================================
         Generate an EnumCallable of Integers.
        ========================================================================
        """
        class EnumCallableA(EnumCallable):
            A = GenEnumCallable.A
            B = GenEnumCallable.B
            C = GenEnumCallable.C
        return EnumCallableA
