from f_data_structure.closed import Closed
from f_data_structure.nodes.node_2_cell import NodeCell


def test_push():
    node_a = NodeCell(name='A', row=1)
    node_b = NodeCell(name='B', row=2)
    closed = Closed()
    closed.push(node_b)
    closed.push(node_a)
    # Insertion Order
    assert closed.items() == [node_b, node_a]


def test_get():
    node = NodeCell(name='A', row=1)
    closed = Closed()
    closed.push(node)
    # Did not remove the item
    assert closed.items() == [node]


def test_contains():
    node = NodeCell(name='A', row=1)
    closed = Closed()
    closed.push(node)
    # Insertion Order
    assert node in closed
