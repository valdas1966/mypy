from anytree import NodeMixin
from f_abstract.mixins.nameable import Nameable


class Node(NodeMixin, Nameable):

    def __init__(self, name: str = None) -> None:
        NodeMixin.__init__(self)
        Nameable.__init__(self, name=name)


a = Node(name='A')
b = Node(name='A')
print(a == b)