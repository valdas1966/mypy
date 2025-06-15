from f_gui_old.shapes.generators.g_1_rect import GenRect


def test_rect() -> None:
    """
    =======================================================================
     Test the Rect-Shape.
    =======================================================================
    """
    rect = GenRect.full()
    assert rect.name == 'Rect'
    assert rect.position.absolute == (0, 0, 100, 100)
    assert rect.position == (0, 0, 100, 100)
