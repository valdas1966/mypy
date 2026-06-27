import tempfile
from pathlib import Path

from f_gui.render.html.main import RenderHtml
from f_gui.elements.i_2_window.main import Window
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_gui.elements.i_1_line.main import Line
from f_gui.style.stroke import Stroke, DashPattern
from f_gui.style.border import Border
from f_ds.geometry.bounds import Bounds
from f_ds.geometry.pointxy import PointXY
from f_color.rgb import RGB


def test_element_label_has_text() -> None:
    """
    ========================================================================
     Test that a Label's text appears in the rendered HTML.
    ========================================================================
    """
    html = RenderHtml.element(elem=Label(text='Hi'))
    assert '>Hi<' in html


def test_element_label_escapes_text() -> None:
    """
    ========================================================================
     Test that special characters in Label text are HTML-escaped.
    ========================================================================
    """
    html = RenderHtml.element(elem=Label(text='<script>'))
    assert '<script>' not in html
    assert '&lt;script&gt;' in html


def test_element_background_renders_hex() -> None:
    """
    ========================================================================
     Test that a set background renders as a CSS hex color.
    ========================================================================
    """
    html = RenderHtml.element(elem=Label(text='Hi',
                                         background=RGB(name='steelblue')))
    assert 'background:#4682B4' in html


def test_element_no_background_by_default() -> None:
    """
    ========================================================================
     Test that no background CSS is emitted when none is set.
    ========================================================================
    """
    html = RenderHtml.element(elem=Label(text='Hi'))
    assert 'background:' not in html


def test_element_uses_percent_bounds() -> None:
    """
    ========================================================================
     Test that bounds are written as CSS percentages.
    ========================================================================
    """
    elem = Container(bounds=Bounds(top=10, left=20, bottom=60, right=80))
    html = RenderHtml.element(elem=elem)
    assert 'top:10%' in html
    assert 'left:20%' in html
    assert 'bottom:40%' in html     # 100 - 60
    assert 'right:20%' in html      # 100 - 80


def test_element_nested_tree() -> None:
    """
    ========================================================================
     Test a nested Window > Container > Label renders 3 <div> elements.
    ========================================================================
    """
    win = Window.Factory.default()
    panel = Container(bounds=Bounds(top=10, left=10, bottom=50, right=50))
    label = Label(bounds=Bounds(top=20, left=20, bottom=80, right=80),
                  text='X')
    win.add_child(child=panel)
    panel.add_child(child=label)
    html = RenderHtml.element(elem=win)
    assert html.count('<div') == 3
    assert '>X<' in html


def test_page_has_doctype() -> None:
    """
    ========================================================================
     Test that page() emits a full HTML document.
    ========================================================================
    """
    page = RenderHtml.page(root=Window.Factory.default())
    assert page.startswith('<!doctype html>')
    assert '</body></html>' in page


def test_to_file_writes_document() -> None:
    """
    ========================================================================
     Test that to_file writes a non-empty HTML page to disk.
    ========================================================================
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'out.html'
        RenderHtml.to_file(root=Window.Factory.default(), path=str(path))
        content = path.read_text()
        assert '<!doctype html>' in content
        assert '<div' in content


def test_line_renders_svg() -> None:
    """
    ========================================================================
     Test that a Line renders as an <svg> with a <line> at % endpoints.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(p1=PointXY(x=10, y=20),
                                        p2=PointXY(x=80, y=90)))
    assert html.startswith('<svg')
    assert '<line ' in html
    assert 'x1="10%"' in html
    assert 'y1="20%"' in html
    assert 'x2="80%"' in html
    assert 'y2="90%"' in html


def test_line_color_renders_hex() -> None:
    """
    ========================================================================
     Test that a Line's stroke color renders as a CSS hex stroke.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(
        p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100),
        stroke=Stroke(color=RGB(name='steelblue'))))
    assert 'stroke="#4682B4"' in html


def test_line_width() -> None:
    """
    ========================================================================
     Test that a Line's stroke width renders as stroke-width.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(
        p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100),
        stroke=Stroke(width=4)))
    assert 'stroke-width="4"' in html


def test_line_solid_has_no_dasharray() -> None:
    """
    ========================================================================
     Test that a solid Line emits no stroke-dasharray.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(p1=PointXY(x=0, y=0),
                                        p2=PointXY(x=100, y=100)))
    assert 'stroke-dasharray' not in html


def test_line_dashed_has_dasharray() -> None:
    """
    ========================================================================
     Test that a dashed Line emits a stroke-dasharray.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(
        p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100),
        stroke=Stroke(pattern=DashPattern.DASHED)))
    assert 'stroke-dasharray="8 6"' in html


def test_line_arrow_emits_marker() -> None:
    """
    ========================================================================
     Test that an arrow Line emits a <marker> and references it.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(p1=PointXY(x=0, y=0),
                                        p2=PointXY(x=100, y=0), arrow=True))
    assert '<marker ' in html
    assert 'marker-end="url(#arrow-' in html


def test_line_no_arrow_no_marker() -> None:
    """
    ========================================================================
     Test that a Line without an arrow emits no <marker>.
    ========================================================================
    """
    html = RenderHtml.element(elem=Line(p1=PointXY(x=0, y=0),
                                        p2=PointXY(x=100, y=0)))
    assert '<marker' not in html
    assert 'marker-end' not in html


def test_line_in_tree() -> None:
    """
    ========================================================================
     Test that a Line nested under a Window renders inside the tree.
    ========================================================================
    """
    win = Window.Factory.default()
    win.add_child(child=Line(p1=PointXY(x=0, y=0), p2=PointXY(x=100, y=100)))
    html = RenderHtml.element(elem=win)
    assert '<svg' in html
    assert '<line ' in html


def test_no_border_by_default() -> None:
    """
    ========================================================================
     Test that an Element with no Border emits no border CSS.
    ========================================================================
    """
    html = RenderHtml.element(elem=Container())
    # box-sizing:border-box is always present; assert no border-<side> decls.
    assert 'border-top' not in html
    assert 'border-right' not in html
    assert 'border-bottom' not in html
    assert 'border-left' not in html


def test_border_uniform_renders_four_sides() -> None:
    """
    ========================================================================
     Test that a uniform Border emits all four per-side declarations.
    ========================================================================
    """
    border = Border.Factory.all(stroke=Stroke(color=RGB(name='RED'), width=2))
    html = RenderHtml.element(elem=Container(border=border))
    assert 'border-top:2px solid #FF0000;' in html
    assert 'border-right:2px solid #FF0000;' in html
    assert 'border-bottom:2px solid #FF0000;' in html
    assert 'border-left:2px solid #FF0000;' in html


def test_border_per_side() -> None:
    """
    ========================================================================
     Test that only set sides emit border CSS (dashed maps to CSS keyword).
    ========================================================================
    """
    border = Border(top=Stroke(width=3, pattern=DashPattern.DASHED))
    html = RenderHtml.element(elem=Container(border=border))
    assert 'border-top:3px dashed #e6edf3;' in html
    assert 'border-bottom' not in html
    assert 'border-left' not in html
    assert 'border-right' not in html


def test_border_style_keywords() -> None:
    """
    ========================================================================
     Test that DashPattern maps 1:1 to the CSS border-style keyword.
    ========================================================================
    """
    border = Border(top=Stroke(pattern=DashPattern.DOTTED))
    html = RenderHtml.element(elem=Container(border=border))
    assert 'border-top:1px dotted ' in html


def test_window_to_html() -> None:
    """
    ========================================================================
     Test the Window.to_html() convenience method.
    ========================================================================
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'win.html'
        Window.Factory.default().to_html(path=str(path))
        assert path.exists()
        assert path.read_text().startswith('<!doctype html>')
