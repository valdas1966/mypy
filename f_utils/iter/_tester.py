from f_utils.iter._factory import Factory
from f_utils.iter import u_iter


def test_sample() -> None:
    """
    ========================================================================
     Test the sample function.
    ========================================================================
    """
    data = Factory.ab()
    pct = 50
    sample = u_iter.sample(data=data, pct=pct)
    assert len(sample) == 1
    
    
def test_filter() -> None:
    """
    ========================================================================
     Test the filter function.
    ========================================================================
    """
    data = Factory.ab()
    predicate = lambda x: x == 'a'
    filtered = u_iter.filter(data=data, predicate=predicate)
    assert len(filtered) == 1
    assert filtered[0] == 'a'
