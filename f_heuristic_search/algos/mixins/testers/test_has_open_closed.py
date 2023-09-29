from f_heuristic_search.algos.mixins.has_open_closed import HasOpenClosed
from f_data_structure.mixins.has_row_col import HasRowCol


def test_open():
    algo = HasOpenClosed()
    rc_1 = HasRowCol(1)
    rc_2 = HasRowCol(2)
    algo.open.put(rc_2)
    algo.open.put(rc_1)
    assert algo.open.get() == rc_1


def test_closed():
    algo = HasOpenClosed()
    rc_1 = HasRowCol(1)
    rc_2 = HasRowCol(2)
    algo.closed.add(rc_2)
    algo.closed.add(rc_1)
    assert list(algo.closed) == [rc_2, rc_1]
