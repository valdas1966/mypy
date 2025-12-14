from f_utils.iter._factory import Factory
from f_utils.iter import u_iter


def test_sample() -> None:
    """
    ========================================================================
     Test the sample function.
    ========================================================================
    """
    data = Factory.abcd()
    pct = 50
    sample = u_iter.sample(data=data, pct=pct)
    assert len(sample) == 2
    
    
def test_filter() -> None:
    """ 
    ========================================================================
     Test the filter function.
    ========================================================================
    """
    data = Factory.abcd()
    predicate = lambda x: x == 'a'
    filtered = u_iter.filter(data=data, predicate=predicate)
    assert len(filtered) == 1
    assert filtered[0] == 'a'


def test_pairs() -> None:
    """
    ========================================================================
     Test the pairs function.
    ========================================================================
    """
    data = Factory.abcd()
    size = 1
    predicate = lambda x, y: x == 'a' and y == 'b'
    pairs = u_iter.pairs(data=data, size=size, predicate=predicate)
    assert pairs == [('a', 'b')]
