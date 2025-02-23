from f_file.generators.g_map_grid import GenMapGrid
import numpy as np


def test_map_grid():
    """
    ========================================================================
     Test the MapGrid object.
    ========================================================================
    """
    map_grid = GenMapGrid.map_grid()
    array = np.array([[True, True, True],
                      [True, False, True],
                      [True, True, True]])
    assert np.array_equal(map_grid.to_array(), array)
