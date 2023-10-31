from f_data_structure.open import Open
from f_data_structure.nodes.node_2_cell import NodeCell


def tester_push():
    cell_a = NodeCell(name='A', row=2)
    cell_b = NodeCell(name='B', row=1)
    open = Open()
    open.push(item=cell_a)
    open.push(item=cell_b)
    assert open.items() == [cell_a, cell_b]


def tester_pop():
    cell_a = NodeCell(name='A', row=2)
    cell_b = NodeCell(name='B', row=1)
    open = Open()
    open.push(item=cell_a)
    open.push(item=cell_b)
    assert open.pop() == cell_b
    assert open.items() == [cell_a]


def test_get():
    cell_a = NodeCell(name='A', row=2)
    cell_b = NodeCell(name='B', row=1)
    open = Open()
    open.push(item=cell_a)
    open.push(item=cell_b)
    assert open.get(cell_a) == cell_a
    assert open.items() == [cell_a, cell_b]


def test_contains():
    cell_a = NodeCell(name='A', row=2)
    cell_b = NodeCell(name='B', row=1)
    open = Open()
    open.push(cell_a)
    open.push(cell_b)
    assert cell_a in open
