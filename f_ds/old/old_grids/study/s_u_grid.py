from f_ds.old_grids.u_grid import UGrid


grid = UGrid.without_header(rows=4, pct_valid=75)
print(grid)
print(len(grid))
print(list(grid.cells_valid))
