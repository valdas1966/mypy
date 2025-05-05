from f_color.factories.f_rgb import FactoryRGB
from f_color.rgb import RGB


def test_from_ints():
    """
    ========================================================================
     Test the from_ints() method of the FactoryRGB-class.
    ========================================================================
    """ 
    rgb = FactoryRGB.from_ints(r=255, g=0, b=0)
    assert rgb == RGB(r=1, g=0, b=0)


def test_from_hex():
    """
    ========================================================================
     Test the from_hex() method of the FactoryRGB-class.
    ========================================================================
    """
    rgb = FactoryRGB.from_hex('#000000')
    assert rgb == RGB(r=0, g=0, b=0)


def test_gradient():
    """
    ========================================================================
     Test the gradient() method of the FactoryRGB-class.
    ========================================================================
    """
    white = RGB(name='WHITE')
    black = RGB(name='BLACK')
    rgb = FactoryRGB.gradient(a=white, b=black, n=5)
    assert rgb[0] == RGB(r=1, g=1, b=1)
    assert rgb[1] == RGB(r=0.75, g=0.75, b=0.75)
    assert rgb[2] == RGB(r=0.5, g=0.5, b=0.5)
    assert rgb[3] == RGB(r=0.25, g=0.25, b=0.25)
    assert rgb[4] == RGB(r=0, g=0, b=0)
