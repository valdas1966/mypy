from f_ds.grids.u_grid import UGrid


def test_generate():
    grid = UGrid.generate(rows=10, pct_valid=90)
    assert len(grid) == 90