from f_ds.grids.grid import Grid


grid = Grid(2, 3)
print(grid)

print(grid.neighbors(grid[0][0]))