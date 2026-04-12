import tempfile
from pathlib import Path

from f_gui.render.html.main import RenderHtml
from f_gui.elements.i_2_window.main import Window
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_ds.geometry.bounds import Bounds


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
