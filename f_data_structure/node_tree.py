
class Node:

    def __init__(self, name, data=None, children=set()):
        self.name = name
        self.data = data
        self.children = children
        self.depth = 0

    def add(self, node):
        self.children.add(node)

    def set_depth(self, depth):
        self.depth = depth

    def get_descendants(self):
        descendants = list()
        opened = [self]
        while opened:
            print('opened')
            print([n.name for n in opened])
            node = opened.pop(0)
            descendants.append(node)
            print('node.children')
            print(list(n.name for n in node.children))
            opened.extend(list(node.children))
            if len(opened) > 5:
                break
        return descendants

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return len(self.name) * len(self.children) * self.depth
