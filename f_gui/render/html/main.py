from html import escape
from pathlib import Path

from f_gui.elements.i_0_element.main import Element
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_gui.elements.i_2_window.main import Window


class RenderHtml:
    """
    ============================================================================
     Renders an f_gui Element tree as a self-contained HTML string.
    ============================================================================
    """

    # Factory
    Factory: type = None

    # Per-type border styles (Window checked before Container since Window IS-A
    # Container). Kept here so the emitter stays stateless.
    _BORDER_WINDOW = '3px solid #ff8c42'
    _BORDER_CONTAINER = '2px dashed #58a6ff'
    _BORDER_LABEL = '2px solid #bc8cff'
    _BORDER_ELEMENT = '1px solid #888'

    @staticmethod
    def element(elem: Element) -> str:
        """
        ========================================================================
         Render the Element (and its descendants) as a single <div> string.
        ========================================================================
        """
        b = elem.bounds
        border = RenderHtml._border(elem=elem)
        style = (f'position:absolute;'
                 f'top:{b.top}%;left:{b.left}%;'
                 f'bottom:{100 - b.bottom}%;right:{100 - b.right}%;'
                 f'box-sizing:border-box;border:{border};'
                 f'display:flex;align-items:center;justify-content:center;'
                 f'overflow:hidden;font-family:monospace;font-size:12px;')
        inner = RenderHtml._inner(elem=elem)
        return f'<div style="{style}">{inner}</div>'

    @staticmethod
    def page(root: Element, size: int = 600) -> str:
        """
        ========================================================================
         Wrap the Element tree in a full HTML document with a sized stage.
        ========================================================================
        """
        body = RenderHtml.element(elem=root)
        return (f'<!doctype html><html><body '
                f'style="margin:0;background:#0d1117;color:#e6edf3;">'
                f'<div style="position:relative;'
                f'width:{size}px;height:{size}px;'
                f'margin:20px auto;background:#161b22;">'
                f'{body}</div></body></html>')

    @staticmethod
    def to_file(root: Element, path: str, size: int = 600) -> None:
        """
        ========================================================================
         Write the rendered HTML page to the given file path.
        ========================================================================
        """
        Path(path).write_text(data=RenderHtml.page(root=root, size=size),
                              encoding='utf-8')

    @staticmethod
    def _border(elem: Element) -> str:
        """
        ========================================================================
         Pick a border style based on the Element's concrete type.
        ========================================================================
        """
        if isinstance(elem, Window):
            return RenderHtml._BORDER_WINDOW
        if isinstance(elem, Container):
            return RenderHtml._BORDER_CONTAINER
        if isinstance(elem, Label):
            return RenderHtml._BORDER_LABEL
        return RenderHtml._BORDER_ELEMENT

    @staticmethod
    def _inner(elem: Element) -> str:
        """
        ========================================================================
         Build the inner HTML: children for Containers, escaped text for Labels.
        ========================================================================
        """
        if isinstance(elem, Container):
            return ''.join(RenderHtml.element(elem=c) for c in elem.children)
        if isinstance(elem, Label):
            return escape(elem.text)
        return ''
