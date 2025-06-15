from f_gui.components.generators.g_component import GenComponent
from f_gui.layout.generators.g_rect import GenRect


def test_window_empty() -> None:
    """
    ========================================================================
     Test the empty window component.
    ========================================================================
    """
    win = GenComponent.window_empty()
    assert win.parent is None
    assert win.children == dict()
    bounds_full = GenRect.full()
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
    assert con.bounds.absolute == GenRect.half()


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
    assert label.bounds.absolute == GenRect.quarter()
