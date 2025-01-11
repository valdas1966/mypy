from f_ds.nodes.i_1_prev_next import NodePrevNext


node = NodePrevNext(uid='A')
print(node)

cloned = node.clone()
print(cloned)
