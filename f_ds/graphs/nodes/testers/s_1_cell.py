from f_ds.graphs.nodes.i_2_cell import NodeCell, Cell


zero = NodeCell(name='Zero')
print(zero)

one = NodeCell(name='One', cell=Cell(1))
print(one)