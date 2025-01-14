from f_graph.path.node import NodePath


a = NodePath(uid='Node', h=1)
b = NodePath(uid='Node', h=2)

print([a] == [b])