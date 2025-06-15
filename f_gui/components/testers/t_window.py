from f_gui.components.window import Window
from f_gui.layout.generators.g_rect import GenRect


def test_window() -> None:
    """
    ========================================================================
     Test the Window.
    ========================================================================
    """
    win = Window()
    assert win.name == 'Window'
    assert win.parent is None
    assert win.children == dict()
    rect_full = GenRect.full()
    assert win.bounds.absolute == rect_full

