from f_gui.components.generators.g_component import GenComponent
from f_gui.geometry.generators.g_bounds import GenBounds


def test_full():
    """
    ========================================================================
     Test the full-screen component.
    ========================================================================
    """
    c_full = GenComponent.full()
    assert c_full.parent is None
    assert c_full.children == dict()
    bounds_full = GenBounds.full()
    assert c_full.geometry.bounds_absolute == bounds_full
