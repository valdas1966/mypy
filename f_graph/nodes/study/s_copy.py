from f_graph.nodes.i_1_path import NodePath as Node
import copy


a = Node('A')
b = Node('B')
b.parent = a

c = copy.deepcopy(b)

print(c, c.parent)
