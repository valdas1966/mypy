from study.generic.s_typevar_abc import A
from typing import Generic, TypeVar

T = TypeVar('T', bound=A)


class D(Generic[T]):
    def __init__(self, t: T):
        self.t = t
    def __str__(self):
        return str(self.t)
