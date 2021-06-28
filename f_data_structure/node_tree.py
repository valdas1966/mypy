
class Node:

    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.children = set()

    def get_descendants(self):
        descendants = list()
        opened = [self]
        while opened:
            node = opened.pop(0)
            descendants.append(node)
            opened.extend(list(node.children))
        return descendants

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return len(self.name) * len(self.children)
