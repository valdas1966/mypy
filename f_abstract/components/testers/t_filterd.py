from f_abstract.components.filtered import Filtered
from f_utils.dtypes.u_int import UInt


def test():
    items = [1, 2]
    s = Filtered(items=items, predicate=UInt.is_even)
    assert s
    assert s.to_list() == [2]
    assert len(s) == 1
    assert s.pct() == 50
