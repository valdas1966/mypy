from f_gui.elements.i_1_connector.main import Connector, Routing
from f_gui.elements.i_1_container.main import Container
from f_gui.style.stroke import Stroke, LineStyle
from f_ds.geometry.bounds import Bounds
from f_ds.geometry.side import Side


def _src() -> Container:
    """
    ========================================================================
     A top-left source Container (center at (20, 30)).
    ========================================================================
    """
    return Container(bounds=Bounds(top=20, left=10, bottom=40, right=30))


def _dst() -> Container:
    """
    ========================================================================
     A bottom-right destination Container (center at (80, 70)).
    ========================================================================
    """
    return Container(bounds=Bounds(top=60, left=70, bottom=80, right=90))


def test_endpoints() -> None:
    """
    ========================================================================
     Test that src / dst references are stored.
    ========================================================================
    """
    a, b = _src(), _dst()
    c = Connector(src=a, dst=b)
    assert c.src is a
    assert c.dst is b


def test_defaults() -> None:
    """
    ========================================================================
     Test default sides (auto), arrow (True) and routing (DIRECT).
    ========================================================================
    """
    c = Connector(src=_src(), dst=_dst())
    assert c.src_side is None
    assert c.dst_side is None
    assert c.arrow is True
    assert c.routing is Routing.DIRECT


def test_stroke_stored() -> None:
    """
    ========================================================================
     Test that a provided Stroke is stored.
    ========================================================================
    """
    stroke = Stroke(width=3, style=LineStyle.DASHED)
    c = Connector(src=_src(), dst=_dst(), stroke=stroke)
    assert c.stroke is stroke


def test_path_direct() -> None:
    """
    ========================================================================
     Test the DIRECT path: the two auto-picked side anchors.
    ========================================================================
     src center (20,30) is left-and-above dst center (80,70): horizontal
     gap dominates -> src.RIGHT (30,30) -> dst.LEFT (70,70).
    ========================================================================
    """
    c = Connector(src=_src(), dst=_dst())
    pts = [p.to_tuple() for p in c.path]
    assert pts == [(30, 30), (70, 70)]


def test_explicit_sides() -> None:
    """
    ========================================================================
     Test that explicit sides override the auto-pick.
    ========================================================================
    """
    c = Connector(src=_src(), dst=_dst(),
                  src_side=Side.TOP, dst_side=Side.TOP)
    pts = [p.to_tuple() for p in c.path]
    # src TOP = (center-x 20, top 20); dst TOP = (center-x 80, top 60).
    assert pts == [(20, 20), (80, 60)]


def test_path_orthogonal_axis_aligned() -> None:
    """
    ========================================================================
     Test that the ORTHOGONAL path is a 90-degree (axis-aligned) elbow.
    ========================================================================
     Endpoints match the anchors; every segment is horizontal or vertical.
    ========================================================================
    """
    c = Connector(src=_src(), dst=_dst(), routing=Routing.ORTHOGONAL)
    pts = c.path
    assert pts[0].to_tuple() == (30, 30)     # src.RIGHT anchor
    assert pts[-1].to_tuple() == (70, 70)    # dst.LEFT anchor
    for a, b in zip(pts, pts[1:]):
        assert a.x == b.x or a.y == b.y      # each segment axis-aligned


def test_bounds_is_bbox() -> None:
    """
    ========================================================================
     Test that bounds is the bounding box of the path (live).
    ========================================================================
    """
    c = Connector(src=_src(), dst=_dst())
    assert c.bounds.to_tuple() == (30, 30, 70, 70)


def test_follows_movement() -> None:
    """
    ========================================================================
     Test that the path is recomputed live (no manual refresh needed).
    ========================================================================
     The same Connector reports different anchors when the destination's
     center moves above the source (vertical gap now dominates).
    ========================================================================
    """
    a = _src()
    b = Container(bounds=Bounds(top=60, left=10, bottom=80, right=30))
    c = Connector(src=a, dst=b)
    # b is directly below a -> vertical gap dominates: a.BOTTOM -> b.TOP.
    pts = [p.to_tuple() for p in c.path]
    assert pts == [(20, 40), (20, 60)]


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    a = Container(bounds=Bounds(top=20, left=10, bottom=40, right=30),
                  name='A')
    b = Container(bounds=Bounds(top=60, left=70, bottom=80, right=90),
                  name='B')
    assert str(Connector(src=a, dst=b)) == 'Connector(A->B)'


def test_factory_orthogonal() -> None:
    """
    ========================================================================
     Test the Factory.orthogonal() preset routing.
    ========================================================================
    """
    assert Connector.Factory.orthogonal().routing is Routing.ORTHOGONAL
