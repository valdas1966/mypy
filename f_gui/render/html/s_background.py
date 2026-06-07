"""Study: Background — fill color (RGB) of an Element.

Top    : a grid of named colors (each swatch labeled).
Middle : a red -> blue gradient via RGB.Factory.gradient.
Bottom : transparent (no background) next to a filled one.

Run:  python -m f_gui.render.html.s_background   (then open background.html)
"""
from f_gui.elements import Window, Container, Label
from f_gui.style import Stroke, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds
from f_color import RGB


def cell(r: int, c: int, rows: int, cols: int,
         top0: float, bot0: float, pad: float = 1.5) -> Bounds:
    h = (bot0 - top0) / rows
    w = 100 / cols
    return Bounds(top=top0 + r * h + pad, left=c * w + pad,
                  bottom=top0 + (r + 1) * h - pad, right=(c + 1) * w - pad)


def swatch(bounds: Bounds, color: RGB | None, text: str) -> Container:
    border = Border.Factory.all(stroke=Stroke(color=RGB('black'), width=1))
    con = Container(bounds=bounds, background=color, border=border)
    con.add_child(Label(text=text))
    return con


win = Window(background=RGB('white'))

# ── Named-color grid (2 x 4) ──────────────────────────────────────────
colors = ['crimson', 'orange', 'gold', 'green',
          'teal', 'steelblue', 'purple', 'violet']
for i, name in enumerate(colors):
    r, c = divmod(i, 4)
    win.add_child(swatch(cell(r, c, 2, 4, top0=3, bot0=52),
                         RGB(name), name))

# ── Gradient strip (1 x 8): red -> blue ───────────────────────────────
grad = RGB.Factory.gradient(a=RGB('red'), b=RGB('blue'), n=8)
for i, color in enumerate(grad):
    win.add_child(swatch(cell(0, i, 1, 8, top0=58, bot0=78), color, ''))
win.add_child(Label(bounds=Bounds(79, 0, 84, 100),
                    text='gradient: RGB.Factory.gradient(red, blue, 8)'))

# ── Transparent vs filled ─────────────────────────────────────────────
win.add_child(swatch(Bounds(86, 2, 98, 49), None, 'transparent (None)'))
win.add_child(swatch(Bounds(86, 51, 98, 98), RGB('gold'), 'filled'))

RenderHtml.to_file(root=win, path='background.html')
