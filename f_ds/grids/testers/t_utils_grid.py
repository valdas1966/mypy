from f_ds.grids.utils_grid import UtilsGrid


def test_generate():
    grid = UtilsGrid.generate(rows=10, pct_valid=90)
    assert len(grud)