from f_hs.nodes.i_1_g import NodeG


a = NodeG(name='a')
a._g = 10
b = NodeG(name='b')
b._g = 5
c = NodeG(name='c', parent=a)
c.update_parent_if_needed(parent=c)
print(c.parent == a)
c.update_parent_if_needed(parent=b)
print(c.parent == b)
