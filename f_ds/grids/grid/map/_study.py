from f_ds.grids.grid.map import GridMap


grid = GridMap.Factory.x()
cell_00 = grid[0][0]
cell_01 = grid[0][1]
print(cell_00, bool(cell_00))
print(cell_01, bool(cell_01))

neighbors = grid.neighbors(cell=grid[1][1])
for n in neighbors:
    print(n, bool(n))