from f_data_structure.f_grid.grid_cells import GridCells


grid = GridCells(2, 3)
print(grid)

grid = GridCells.generate(rows=5, pct_non_valid=20)
print(grid)