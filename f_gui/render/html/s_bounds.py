"""Study: Bounds — the 0-100 coordinate system.

Left panel  : children positioned RELATIVE to their parent (not the window)
              + the four corners.
Right panel : concentric full -> half -> quarter, showing the scale + nesting.

Run:  python -m f_gui.render.html.s_bounds   (then open bounds.html)
"""
from f_gui.elements import Window, Container, Label
from f_gui.style import Stroke, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds
from f_color import RGB


def thin(color: str) -> Border:
    return Border.Factory.all(stroke=Stroke(color=RGB(color), width=1))


def box(bounds: Bounds, text: str, color: str, border: str = 'black') -> Container:
    con = Container(bounds=bounds, background=RGB(color), border=thin(border))
    con.add_child(Label(text=text))
    return con


win = Window(background=RGB('white'))

# ── Left panel: a parent, with children placed relative to IT ──────────
parent = Container(bounds=Bounds(top=6, left=3, bottom=94, right=48),
                   background=RGB('whitesmoke'), border=thin('black'))
parent.add_child(Label(bounds=Bounds(0, 0, 12, 100), text='parent (rel. to me)'))
# Corners — coordinates are within the parent, not the window.
parent.add_child(box(Bounds(14, 4, 34, 40), 'TL (14,4,34,40)', 'lightcoral'))
parent.add_child(box(Bounds(14, 60, 34, 96), 'TR', 'lightsalmon'))
parent.add_child(box(Bounds(66, 4, 86, 40), 'BL', 'khaki'))
parent.add_child(box(Bounds(66, 60, 86, 96), 'BR', 'lightgreen'))
parent.add_child(box(Bounds(42, 30, 58, 70), 'center', 'lightblue'))
win.add_child(parent)

# ── Right panel: concentric full -> half -> quarter ───────────────────
full = Container(bounds=Bounds(top=6, left=52, bottom=94, right=97),
                 background=RGB('whitesmoke'), border=thin('black'))
full.add_child(Label(bounds=Bounds(0, 0, 10, 100), text='full (0,0,100,100)'))
half = box(Bounds(25, 25, 75, 75), '', 'lightblue', 'steelblue')
half.add_child(Label(bounds=Bounds(0, 0, 16, 100), text='half (25,25,75,75)'))
quarter = box(Bounds(37.5, 37.5, 62.5, 62.5),
              'quarter', 'lightsteelblue', 'navy')
half.add_child(quarter)
full.add_child(half)
win.add_child(full)

RenderHtml.to_file(root=win, path='bounds.html')
