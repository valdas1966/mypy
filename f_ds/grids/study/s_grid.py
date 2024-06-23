from f_ds.grids.grid import Grid


def print_grid():
    print(grid)


def print_neighbors():
    print(grid.neighbors(grid[0][0]))


def print_cells_valid():
    print(list(grid.cells_valid))
    print(grid.cells_valid.cnt())


grid = Grid(2, 3)
grid[1][1].set_invalid()

# print_grid()
# print_neighbors()
print_cells_valid()
