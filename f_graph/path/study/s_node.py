from f_graph.node import NodeGraph


class Node(NodeGraph[int]):

    def __init__(self, uid: int, val: int) -> None:
        NodeGraph.__init__(self, uid=uid)
        self.val = val

    def key_comparison(self) -> list:
        return [self.val]


a = Node(uid=1, val=2)
b = Node(uid=1, val=3)

print(a == b)
print(a < b)
print(a > b)
