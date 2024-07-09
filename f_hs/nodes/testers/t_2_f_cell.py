from f_hs.nodes.i_2_f_cell import NodeFCell


def test_repr():
    node = NodeFCell(name='A')
    node.h = 5
    assert repr(node) == '<NodeFCell: A(0,0)> G=0, H=5, F=5'
