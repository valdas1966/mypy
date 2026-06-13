from html import escape
from pathlib import Path

from f_gui.elements.i_0_element.main import Element
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_gui.elements.i_1_line.main import Line
from f_gui.elements.i_1_connector.main import Connector
from f_gui.style.stroke import LineStyle


class RenderHtml:
    """
    ============================================================================
     Renders an f_gui Element tree as a self-contained HTML string.
    ============================================================================
    """

    # Factory
    Factory: type = None

    # Fallback color when a Stroke (Line or Border edge) carries no color.
    _STROKE_DEFAULT = '#e6edf3'

    # SVG stroke-dasharray per LineStyle (solid -> no dasharray).
    _DASH = {LineStyle.DASHED: '8 6', LineStyle.DOTTED: '1 6'}

    @staticmethod
    def element(elem: Element) -> str:
        """
        ========================================================================
         Render the Element (and its descendants) as a single HTML string.
        ========================================================================
         A Line emits an <svg> overlay; every other Element emits a <div>.
        ========================================================================
        """
        if isinstance(elem, Line):
            return RenderHtml._line(elem=elem)
        if isinstance(elem, Connector):
            return RenderHtml._connector(elem=elem)
        b = elem.bounds
        border = RenderHtml._border(elem=elem)
        bg = RenderHtml._background(elem=elem)
        text = RenderHtml._text_style(elem=elem)
        style = (f'position:absolute;'
                 f'top:{b.top}%;left:{b.left}%;'
                 f'bottom:{100 - b.bottom}%;right:{100 - b.right}%;'
                 f'box-sizing:border-box;{border}{bg}'
                 f'display:flex;align-items:center;justify-content:center;'
                 f'overflow:hidden;{text}')
        inner = RenderHtml._inner(elem=elem)
        return f'<div style="{style}">{inner}</div>'

    @staticmethod
    def page(root: Element, size: int | None = None) -> str:
        """
        ========================================================================
         Wrap the Element tree in a full HTML document with a stage.
        ========================================================================
         size=None (default) -> the stage fills the browser viewport
         (full-screen), matching what a Window models. Pass an int for a
         fixed size x size centered square stage (e.g. a thumbnail).
        ========================================================================
        """
        body = RenderHtml.element(elem=root)
        if size is None:
            # Fill the viewport — a Window models the whole screen.
            stage = 'position:fixed;inset:0;background:#161b22;'
        else:
            stage = (f'position:relative;'
                     f'width:{size}px;height:{size}px;'
                     f'margin:20px auto;background:#161b22;')
        return (f'<!doctype html><html>'
                f'<head><meta charset="utf-8"></head>'
                f'<body style="margin:0;background:#0d1117;color:#e6edf3;">'
                f'<div style="{stage}">{body}</div>'
                f'</body></html>')

    @staticmethod
    def to_file(root: Element, path: str, size: int | None = None) -> None:
        """
        ========================================================================
         Write the rendered HTML page to the given file path.
        ========================================================================
        """
        Path(path).write_text(data=RenderHtml.page(root=root, size=size),
                              encoding='utf-8')

    @staticmethod
    def _text_style(elem: Element) -> str:
        """
        ========================================================================
         CSS text declarations (font / size / weight / color) for a Label.
        ========================================================================
         Non-Labels carry no text, so they emit nothing. A Label with no
         `style` emits the baseline default (monospace, 12px, black) — the
         same as `TextStyle()`. font/size/bold/color all map; an explicit
         `color=None` opts out (inherits the page color). Duck-typed:
         RenderHtml imports no TextStyle type (like Border / Stroke).
        ========================================================================
        """
        if not isinstance(elem, Label):
            return ''
        style = elem.style
        if style is None:
            return 'font-family:monospace;font-size:12px;color:#000000;'
        css = f'font-family:{style.font};font-size:{style.size}px;'
        if style.bold:
            css += 'font-weight:bold;'
        if style.color is not None:
            css += f'color:{style.color.to.hex()};'
        return css

    @staticmethod
    def _background(elem: Element) -> str:
        """
        ========================================================================
         CSS background declaration for the Element, or '' if none set.
        ========================================================================
        """
        color = elem.background
        if color is None:
            return ''
        return f'background:{color.to.hex()};'

    @staticmethod
    def _line(elem: Line) -> str:
        """
        ========================================================================
         Render a Line as a self-contained <svg> overlay filling its parent.
        ========================================================================
         Endpoints are percentages of the parent box (0-100 -> SVG %), so a
         diagonal maps exactly onto the scene graph's coordinate space.
         color->stroke, width->stroke-width (px), style->stroke-dasharray,
         arrow->a per-svg <marker> referenced by marker-end.
        ========================================================================
        """
        p1, p2 = elem.p1, elem.p2
        stroke = elem.stroke
        color = RenderHtml._stroke_color(stroke=stroke)
        cap = 'round' if stroke.style is LineStyle.DOTTED else 'butt'
        dash = RenderHtml._dash(style=stroke.style)
        # Arrowhead — id is content-derived so it is unique per distinct Line
        # (duplicate ids across inline SVGs would otherwise collide).
        defs = marker = ''
        if elem.arrow:
            uid = (f'{color}-{p1.x}-{p1.y}-{p2.x}-{p2.y}'
                   .replace('#', '').replace('.', '_'))
            mid = f'arrow-{uid}'
            defs = (f'<defs><marker id="{mid}" markerWidth="10" '
                    f'markerHeight="10" refX="10" refY="5" orient="auto" '
                    f'markerUnits="strokeWidth">'
                    f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/>'
                    f'</marker></defs>')
            marker = f' marker-end="url(#{mid})"'
        line = (f'<line x1="{p1.x}%" y1="{p1.y}%" '
                f'x2="{p2.x}%" y2="{p2.y}%" '
                f'stroke="{color}" stroke-width="{stroke.width}" '
                f'stroke-linecap="{cap}"{dash}{marker}/>')
        style = ('position:absolute;inset:0;width:100%;height:100%;'
                 'overflow:visible;pointer-events:none;')
        return f'<svg style="{style}">{defs}{line}</svg>'

    @staticmethod
    def _connector(elem: Connector) -> str:
        """
        ========================================================================
         Render a Connector as a self-contained <svg> overlay (a polyline).
        ========================================================================
         The live `path` (>= 2 points) becomes a chain of <line> segments —
         the same percent-coordinate SVG model as a single Line, so it is
         distortion-free. The arrowhead (if any) sits on the last segment via
         a per-svg <marker> with a content-derived id (unique per path).
        ========================================================================
        """
        pts = elem.path
        stroke = elem.stroke
        color = RenderHtml._stroke_color(stroke=stroke)
        cap = 'round' if stroke.style is LineStyle.DOTTED else 'butt'
        dash = RenderHtml._dash(style=stroke.style)
        # Arrowhead — id is content-derived (unique per distinct path).
        defs = marker = ''
        if elem.arrow:
            seq = '-'.join(f'{p.x}_{p.y}' for p in pts)
            uid = f'{color}-{seq}'.replace('#', '').replace('.', '_')
            mid = f'arrow-{uid}'
            defs = (f'<defs><marker id="{mid}" markerWidth="10" '
                    f'markerHeight="10" refX="10" refY="5" orient="auto" '
                    f'markerUnits="strokeWidth">'
                    f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/>'
                    f'</marker></defs>')
            marker = f'url(#{mid})'
        last = len(pts) - 1
        segments = ''
        for i in range(last):
            a, b = pts[i], pts[i + 1]
            end = f' marker-end="{marker}"' if marker and i == last - 1 else ''
            segments += (f'<line x1="{a.x}%" y1="{a.y}%" '
                         f'x2="{b.x}%" y2="{b.y}%" '
                         f'stroke="{color}" stroke-width="{stroke.width}" '
                         f'stroke-linecap="{cap}"{dash}{end}/>')
        style = ('position:absolute;inset:0;width:100%;height:100%;'
                 'overflow:visible;pointer-events:none;')
        return f'<svg style="{style}">{defs}{segments}</svg>'

    @staticmethod
    def _dash(style: LineStyle) -> str:
        """
        ========================================================================
         CSS stroke-dasharray attribute for the style, or '' for solid.
        ========================================================================
        """
        pattern = RenderHtml._DASH.get(style)
        if pattern is None:
            return ''
        return f' stroke-dasharray="{pattern}"'

    @staticmethod
    def _stroke_color(stroke) -> str:
        """
        ========================================================================
         Hex color of a Stroke, or the default when it carries no color.
        ========================================================================
        """
        color = stroke.color
        if color is None:
            return RenderHtml._STROKE_DEFAULT
        return color.to.hex()

    @staticmethod
    def _border(elem: Element) -> str:
        """
        ========================================================================
         Per-side CSS border declarations from the Element's Border state.
        ========================================================================
         Border is opt-in: an Element with no border emits nothing. Each set
         side maps 1:1 onto `border-{side}: {width}px {style} {color}` —
         LineStyle values are the exact CSS border-style keywords.
        ========================================================================
        """
        border = elem.border
        if border is None:
            return ''
        sides = (('top', border.top), ('right', border.right),
                 ('bottom', border.bottom), ('left', border.left))
        out = ''
        for side, stroke in sides:
            if stroke is None:
                continue
            color = RenderHtml._stroke_color(stroke=stroke)
            out += (f'border-{side}:{stroke.width}px '
                    f'{stroke.style.value} {color};')
        return out

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
