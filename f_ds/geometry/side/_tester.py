from f_ds.geometry.side.main import Side


def test_members() -> None:
    """
    ========================================================================
     Test the four Side members and their CSS-keyword values.
    ========================================================================
    """
    assert {s.value for s in Side} == {'top', 'right', 'bottom', 'left'}


def test_normal_top() -> None:
    """
    ========================================================================
     Test that TOP's outward normal points up (0, -1).
    ========================================================================
    """
    assert Side.TOP.normal == (0, -1)


def test_normal_right() -> None:
    """
    ========================================================================
     Test that RIGHT's outward normal points right (1, 0).
    ========================================================================
    """
    assert Side.RIGHT.normal == (1, 0)


def test_normal_bottom() -> None:
    """
    ========================================================================
     Test that BOTTOM's outward normal points down (0, 1).
    ========================================================================
    """
    assert Side.BOTTOM.normal == (0, 1)


def test_normal_left() -> None:
    """
    ========================================================================
     Test that LEFT's outward normal points left (-1, 0).
    ========================================================================
    """
    assert Side.LEFT.normal == (-1, 0)


def test_opposite() -> None:
    """
    ========================================================================
     Test the opposing-side pairs (TOP<->BOTTOM, LEFT<->RIGHT).
    ========================================================================
    """
    assert Side.TOP.opposite is Side.BOTTOM
    assert Side.BOTTOM.opposite is Side.TOP
    assert Side.LEFT.opposite is Side.RIGHT
    assert Side.RIGHT.opposite is Side.LEFT
