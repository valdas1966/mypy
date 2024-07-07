from f_hs.nodes.mixins.has_g import NodeG


a = NodeG()
b = NodeG(parent=a)

print(repr(a))
print(repr(b))
print(a > b)