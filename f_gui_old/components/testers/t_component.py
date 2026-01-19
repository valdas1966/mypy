from f_gui_old.components.generators.g_component import GenComponent
from f_gui.layout import FactoryRect


def test_window_empty() -> None:
    """
    ========================================================================
     Test the empty window component.
    ========================================================================
    """
    win = GenComponent.window_empty()
    assert win.parent is None
    assert win.children == dict()
    bounds_full = FactoryRect.full()
    assert win.bounds.absolute == bounds_full


def test_window_container() -> None:
    """
    ========================================================================
     Test the window with one container in the center.
    ========================================================================
    """
    win = GenComponent.window_container()
    con = win.children['Container']
    assert win.parent is None
    assert win.children == {'Container': con}
    assert con.parent == win
    assert con.bounds.absolute == FactoryRect.half()


def test_window_label() -> None:
    """
    ========================================================================
     Test the window with one container and one label in the center.
    ========================================================================
    """
    win = GenComponent.window_label()
    con = win.children['Container']
    label = con.children['Label']       
    assert con.children == {'Label': label}
    assert label.parent == con
    assert label.bounds.absolute == FactoryRect.quarter()
