from f_hs.ds.nodes.i_2_flags import NodeFlags


a = NodeFlags.Factory.a()
a.print_details()   

b = NodeFlags.Factory.b()
b.print_details()

c = NodeFlags.Factory.c()
c.print_details()

d = NodeFlags.Factory.d()
d.print_details()

e = NodeFlags.Factory.e()
e.print_details()
print(d.h, e.h)

f = NodeFlags.Factory.f()
f.print_details()

