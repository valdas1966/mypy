from study.generic.s_typevar_abc import C
from study.generic.s_typevar_f import F


class G(F):
    def __init__(self, t: C):
        self.t = t