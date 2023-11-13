from f_heuristic_search.nodes.i_0_has_cost import NodeHasCost


class Node(NodeHasCost):
    def __init__(self, name: str = None, cost: int = 0) -> None:
        NodeHasCost.__init__(self, name=name)
        self._cost = cost

    def cost(self) -> int:
        return self._cost


def test_cost():
    a = Node(name='A', cost=1)
    b = Node(name='B', cost=2)
    c = Node(name='C', cost=2)
    assert a < b
    assert b == c
