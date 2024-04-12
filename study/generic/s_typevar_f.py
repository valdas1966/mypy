from study.generic.s_typevar_abc import B
from study.generic.s_typevar_d import D


class F(D):
    def __init__(self, t: B):
        D.__init__(self, t=t)
