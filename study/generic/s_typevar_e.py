from study.generic.s_typevar_abc import B
from study.generic.s_typevar_d import D
from typing import Generic, TypeVar

T = TypeVar('T', bound=B)


class E(D[T]):

    def __init__(self, t: T):
        D.__init__(self, t=t)
