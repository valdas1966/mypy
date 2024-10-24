from f_ds.queues.i_1_priority import QueuePriority
from f_graph.nodes.i_0_base import NodeBase


class Node(NodeBase):

    def __init__(self, name: str, val: int) -> None:
        NodeBase.__init__(self, name=name)
        self.val = val

    def key_comparison(self) -> list:
        return [self.val]

    def __repr__(self) -> str:
        return f'{str(self)}({self.val})'


a = Node('A', 1)
b = Node('B', 2)

q = QueuePriority[Node](name='PriorityQueue')
q.push(a)
q.push(b)
print(q)
b.val = 0
q.update()
print(q)
