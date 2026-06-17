"""Study: Border — four edge Strokes around an Element.

Shows solid / dashed / dotted side by side (note: dashed = segments,
dotted = round dots), plus per-side, multi-color, and width variants.

Run:  python -m f_gui.render.html.s_border   (then open border.html)
"""
from f_gui.elements import Window, Container, Label
from f_gui.style import Stroke, DashPattern, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds
from f_color import RGB


def cell(r: int, c: int, pad: float = 2.5) -> Bounds:
    h, w = 100 / 2, 100 / 4
    return Bounds(top=r * h + pad, left=c * w + pad,
                  bottom=(r + 1) * h - pad, right=(c + 1) * w - pad)


def demo(i: int, text: str, border: Border) -> Container:
    r, c = divmod(i, 4)
    con = Container(bounds=cell(r, c), background=RGB('white'), border=border)
    con.add_child(Label(text=text))
    return con


def stroke(color: str, width: float, pattern: DashPattern) -> Stroke:
    return Stroke(color=RGB(color), width=width, pattern=pattern)


win = Window(background=RGB('gainsboro'))

variants = [
    ('solid',   Border.Factory.all(stroke('black', 2, DashPattern.SOLID))),
    ('dashed',  Border.Factory.all(stroke('blue', 2, DashPattern.DASHED))),
    ('dotted',  Border.Factory.all(stroke('green', 2, DashPattern.DOTTED))),
    ('top only', Border(top=stroke('red', 3, DashPattern.SOLID))),
    ('top + bottom',
     Border(top=stroke('purple', 3, DashPattern.SOLID),
            bottom=stroke('purple', 3, DashPattern.SOLID))),
    ('4 colors',
     Border(top=stroke('red', 3, DashPattern.SOLID),
            right=stroke('green', 3, DashPattern.SOLID),
            bottom=stroke('blue', 3, DashPattern.SOLID),
            left=stroke('orange', 3, DashPattern.SOLID))),
    ('thick (6px)', Border.Factory.all(stroke('black', 6, DashPattern.SOLID))),
    ('thin (1px)',  Border.Factory.all(stroke('black', 1, DashPattern.SOLID))),
]
for i, (text, border) in enumerate(variants):
    win.add_child(demo(i, text, border))

RenderHtml.to_file(root=win, path='border.html')
