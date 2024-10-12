from f_ds.grids.grid import Grid


def print_grid():
    print(grid)


def print_neighbors():
    print(grid.neighbors(grid[0][0]))


def print_cells_valid():
    print(list(grid.cells_valid))
    print(len(grid.cells_valid))
    print(grid.cells_valid.pct())
    print(5/6)


grid = Grid(2, 3)
grid[1][1].set_invalid()

print('Grid:')
print_grid()
print('Neighbors:')
print_neighbors()
print()
print('Cells Valid:')
print_cells_valid()
