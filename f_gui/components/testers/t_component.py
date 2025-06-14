from f_gui.components.generators.g_component import GenComponent


def test_full():
    c_full = GenComponent.full()
    assert c_full.parent is None
    assert c_full.children == dict()
    assert c_full.geometry.bounds_absolute.to_tuple == (0, 0, 100, 100)
