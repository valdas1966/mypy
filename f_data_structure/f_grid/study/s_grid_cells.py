from f_data_structure.f_grid.grid_cells import GridCells


grid = GridCells(2, 3)
grid[1][2].name = 'A'
cell = grid.cells()[-1]
print(grid)