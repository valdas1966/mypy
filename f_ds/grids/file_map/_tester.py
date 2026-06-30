from f_ds.grids.file_map import UFileMap
from f_psl.file import u_txt
import numpy as np
import pytest


@pytest.fixture
def path() -> str:
    """
    ========================================================================
     Path to the file-i_1_map.
    ========================================================================
    """
    path = 'g:\\temp\\test.txt'
    lines = list()
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('@@@@@')
    lines.append('@...@')
    lines.append('@.@.@')
    lines.append('@...@')
    lines.append('@@@@@')
    u_txt.from_list(path=path, lines=lines)
    return path


def test_to_bool_array(path: str) -> None:
    """
    ========================================================================
     Test the to_bool_array() method.
    ========================================================================
    """ 
    array_test = UFileMap.to_bool_array(path=path)
    array_true = np.array([[True, True, True],
                           [True, False, True],
                           [True, True, True]])
    assert np.array_equal(array_test, array_true)
