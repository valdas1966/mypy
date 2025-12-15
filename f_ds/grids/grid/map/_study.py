from f_ds.grids.grid.map import GridMap


grid = GridMap.Factory.x()
print(grid)
print(grid.record)
print()

pairs = grid.random.pairs(size=1, min_distance=4)
print(pairs)
