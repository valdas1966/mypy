from f_ds.grids.u_grid import UGrid


grid = UGrid.generate(rows=10, pct_valid=99)
print(grid)