from f_graph.path.elements.node import NodePath as Node


node = Node.generate_zero()
print(node)
print(node.parent)
print(node.path_from_start())