from f_color.rgb import RGB


def test_init():
    """
    ========================================================================
     Test the initialization of the RGB-class.
    ========================================================================
    """
    black_1 = RGB(r=0, g=0, b=0)
    black_2 = RGB(name='BLACK')
    assert black_1 == black_2


def test_to_tuple():
    """
    ========================================================================
     Test the to_tuple method of the RGB-class.
    ========================================================================
    """
    rgb = RGB(name='WHITE')
    assert rgb.to_tuple() == (1, 1, 1)
    assert rgb.to_tuple(to_int=True) == (255, 255, 255)


def test_str():
    """
    ========================================================================
     Test the str method of the RGB-class.
    ========================================================================
    """
    rgb = RGB(r=0.5, g=0.5, b=0.5)
    assert str(rgb) == '(0.5, 0.5, 0.5)'
