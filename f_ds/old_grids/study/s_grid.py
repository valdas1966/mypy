from f_ds.old_grids.old_grid import Grid


grid = Grid.generate(rows=3)
print(grid)

print(grid.neighbors(cell=grid[0][0]))
print(grid.neighbors(cell=grid[0][1]))
