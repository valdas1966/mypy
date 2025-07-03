from f_ds.old_grids.u_grid import UGrid


def test_generate():
    grid = UGrid.gen(rows=10, pct_valid=90)
    assert len(grid) == 100
    assert len(grid.cells_valid) == 90


def test_generate_multiple():
    grids = UGrid.generate_multiple(n=10, rows=10, pct_valid=90)
    assert len(grids) == 10
