from f_core.mixins.has.row_col.main import HasRowCol


def test_zero() -> None:
    """
    ========================================================================
     Test the zero() method.
    ========================================================================
    """
    zero = HasRowCol.Factory.zero()
    assert zero.row == 0
    assert zero.col == 0


def test_one() -> None:
    """
    ========================================================================
     Test the one() method.
    ========================================================================
    """
    one = HasRowCol.Factory.one()
    assert one.row == 1
    assert one.col == 1


def test_twelve() -> None:
    """
    ========================================================================
     Test the twelve() method.
    ========================================================================
    """ 
    twelve = HasRowCol.Factory.twelve()
    assert twelve.row == 1
    assert twelve.col == 2
    
    
def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """ 
    twelve = HasRowCol.Factory.twelve()
    assert twelve.key_comparison() == (1, 2)
    
    
def test_to_tuple() -> None:
    """
    ========================================================================
     Test the to_tuple() method.
    ========================================================================
    """
    twelve = HasRowCol.Factory.twelve()
    assert twelve.to_tuple() == (1, 2)
    
    
def test_neighbors() -> None:
    """
    ========================================================================
     Test the neighbors() method.
    ========================================================================
    """
    twelve = HasRowCol.Factory.twelve()
    neighbors_test = twelve.neighbors()
    neighbors_true = [
                        HasRowCol(row=0, col=2),
                        HasRowCol(row=1, col=3),
                        HasRowCol(row=2, col=2),
                        HasRowCol(row=1, col=1)
                     ]
    assert neighbors_test == neighbors_true


def test_hash() -> None:
    zero = HasRowCol.Factory.zero()
    one = HasRowCol.Factory.one()
    assert hash(zero) != hash(one)
