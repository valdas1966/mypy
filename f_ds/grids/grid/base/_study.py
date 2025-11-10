from f_ds.grids.grid.base.main import GridBase as Grid


grid = Grid(rows=3)

cells = grid.sample(size=2)

print(cells)


