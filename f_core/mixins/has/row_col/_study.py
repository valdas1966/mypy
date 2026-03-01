from f_core.mixins.has import HasRowCol


cell_01 = HasRowCol(0, 1)
cell_10 = HasRowCol(1, 0)

print(cell_01 < cell_10)

