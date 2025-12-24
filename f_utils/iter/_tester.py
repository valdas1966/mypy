from f_ds.pair import Pair
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
    sample = u_iter.sample(items=data, pct=pct)
    assert len(sample) == 2
    
    
def test_filter() -> None:
    """ 
    ========================================================================
     Test the filter function.
    ========================================================================
    """
    data = Factory.abcd()
    predicate = lambda x: x == 'a'
    filtered = u_iter.filter(items=data, predicate=predicate)
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
    predicate = lambda x, y: x == 'a'
    blacklist = [('a', 'c'), ('a', 'd')]
    pairs = u_iter.pairs(items=data,
                         size=size,
                         predicate=predicate,
                         blacklist=blacklist)
    assert pairs == [('a', 'b')]


def test_distribute() -> None:
    """
    ========================================================================
     Test the distribute function.
    ========================================================================
    """
    items = [1, 2, 3, 4]
    keys = ['a', 'b']
    distributed = u_iter.distribute(items=items, keys=keys)
    assert distributed == {'a': [1, 2], 'b': [3, 4]}
