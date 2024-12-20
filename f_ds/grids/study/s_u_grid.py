from f_ds.grids.u_grid import UGrid


grid = UGrid.gen(rows=4, pct_valid=75)
print(grid)
print(len(grid))
print(list(grid.cells_valid))
