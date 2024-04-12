from study.generic.s_typevar_abc import A, B, C
from study.generic.s_typevar_d import D
from study.generic.s_typevar_e import E
from study.generic.s_typevar_f import F
from study.generic.s_typevar_g import G


a = A()
b = B()
c = C()

d = D(b)
print(f'd={str(d)}')
d = D[B](b)
print(f'd={str(d)}')

e = E(b)
print(f'e={str(e)}')
e = D[B](b)
print(f'e={str(e)}')

f = F(b)
print(f'f={str(f)}')
f = F(b)
print(f'f={str(f)}')
print(type(f.t))

g = G(c)
print(f'g={str(g)}')
g = G(c)
print(f'g={str(g)}')
g.t.only_c()