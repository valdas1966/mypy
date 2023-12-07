class NodeA:
    def __init__(self, x):
        self._x = x
    @property
    def x(self):
        return self._x


class NodeB(NodeA):
    @property
    def x(self):
        return self._x * self._x


class A:
    def __init__(self, node: NodeA):
        self._node = node

    def x(self):
        return self._node.x


class B(A):
    def x(self):
        return self._node.x * self._node.x


n_a = NodeA(x=2)
n_b = NodeB(x=2)

c = A[NodeA](node=n_a)
d = B[NodeB](node=n_b)

