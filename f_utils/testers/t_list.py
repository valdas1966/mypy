import pytest
from f_utils import (u_list, u_int)


@pytest.fixture
def ex_10() -> list[int]:
    """
    ============================================================================
     [1:11]
    ============================================================================
    """
    return list(range(1, 11))

def test_to_filter(ex_10):
    evens = u_list.to_filter(li=ex_10, predicate=u_int.is_even)
    assert evens == [2, 4, 6, 8, 10]


def test_to_sample(ex_10):
    # Test: Size
    size = 7
    sample_size = u_list.to_sample(li=ex_10, size=size)
    assert len(sample_size) == size
    # Test: Pct
    pct = 40
    sample_pct = u_list.to_sample(li=ex_10, pct=pct)
    assert len(sample_pct) == 4
    # Test: Predicate
    predicate = u_int.is_even
    sample_predicate = u_list.to_sample(li=ex_10, predicate=predicate, size=5)
    assert set(sample_predicate) == {2, 4, 6, 8, 10}
