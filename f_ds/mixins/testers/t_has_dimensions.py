from f_ds.mixins.has_dimensions import HasDimensions


def test_has_dimensions_init():
    """
    ============================================================================
     Test HasDimensions initialization with default and custom values.
    ============================================================================
    """
    # Test default initialization
    obj = HasDimensions()
    assert obj.width == 100
    assert obj.height == 100

    # Test custom dimensions
    obj = HasDimensions(width=200, height=300)
    assert obj.width == 200
    assert obj.height == 300


def test_has_dimensions_width():
    """
    ============================================================================
     Test width property getter.
    ============================================================================
    """
    obj = HasDimensions(width=150, height=100)
    assert obj.width == 150


def test_has_dimensions_height():
    """
    ============================================================================
     Test height property getter.
    ============================================================================
    """
    obj = HasDimensions(width=100, height=250)
    assert obj.height == 250


def test_has_dimensions_str():
    """
    ============================================================================
     Test string representation of dimensions.
    ============================================================================
    """
    obj = HasDimensions(width=200, height=300)
    assert str(obj) == '(200x300)'

