from f_gui.elements.i_1_line.main import Line
from f_gui.style.stroke import Stroke, DashPattern
from f_ds.geometry.pointxy import PointXY


def test_endpoints() -> None:
    """
    ========================================================================
     Test the p1 / p2 endpoint properties.
    ========================================================================
    """
    line = Line(p1=PointXY(x=10, y=20), p2=PointXY(x=80, y=90))
    assert line.p1.to_tuple() == (10, 20)
    assert line.p2.to_tuple() == (80, 90)


def test_default_stroke() -> None:
    """
    ========================================================================
     Test that a Line gets a default Stroke and no arrow.
    ========================================================================
    """
    line = Line(p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100))
    assert line.stroke.color is None
    assert line.stroke.width == 1
    assert line.stroke.pattern is DashPattern.SOLID
    assert line.arrow is False


def test_stroke_stored() -> None:
    """
    ========================================================================
     Test that a provided Stroke is stored.
    ========================================================================
    """
    stroke = Stroke(width=3, pattern=DashPattern.DASHED)
    line = Line(p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100), stroke=stroke)
    assert line.stroke is stroke


def test_arrow() -> None:
    """
    ========================================================================
     Test that the arrow flag is stored.
    ========================================================================
    """
    line = Line(p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=0), arrow=True)
    assert line.arrow is True


def test_bounds_is_bbox() -> None:
    """
    ========================================================================
     Test that bounds is the bounding box of the two endpoints.
    ========================================================================
    """
    line = Line(p1=PointXY(x=80, y=90), p2=PointXY(x=10, y=20))
    assert line.bounds.to_tuple() == (20, 10, 90, 80)


def test_name() -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert Line.Factory.diagonal().name == 'Line'


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    line = Line(p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100))
    assert str(line) == 'Line(0, 0)->(100, 100)'


def test_parent() -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert Line.Factory.diagonal().parent is None
