from f_gui_old.components.window import Window
from f_gui.layout import FactoryRect


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
    rect_full = FactoryRect.full()
    assert win.bounds.absolute == rect_full

