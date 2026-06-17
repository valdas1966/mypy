"""Study: Line — a directed segment (Stroke + endpoints + arrow).

Shows solid / dashed / dotted (dashed = segments, dotted = round dots),
arrow vs none, the four directions, and width variants. Each line sits in
its own cell so its 0-100 coords are clear; caption at the cell bottom.

Run:  python -m f_gui.render.html.s_line   (then open line.html)
"""
from f_gui.elements import Window, Container, Label, Line
from f_gui.style import Stroke, DashPattern, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds, Point
from f_color import RGB


def cell_bounds(r: int, c: int, pad: float = 2.0) -> Bounds:
    h, w = 100 / 2, 100 / 4
    return Bounds(top=r * h + pad, left=c * w + pad,
                  bottom=(r + 1) * h - pad, right=(c + 1) * w - pad)


def cell(i: int, text: str, line: Line) -> Container:
    r, c = divmod(i, 4)
    edge = Border.Factory.all(stroke=Stroke(color=RGB('black'), width=1))
    con = Container(bounds=cell_bounds(r, c), background=RGB('white'),
                    border=edge)
    con.add_child(line)
    con.add_child(Label(bounds=Bounds(78, 2, 98, 98), text=text))
    return con


def line(x1, y1, x2, y2, color, width=2,
         pattern=DashPattern.SOLID, arrow=False) -> Line:
    return Line(p1=Point(x=x1, y=y1), p2=Point(x=x2, y=y2),
                stroke=Stroke(color=RGB(color), width=width, pattern=pattern),
                arrow=arrow)


win = Window(background=RGB('gainsboro'))

cells = [
    ('solid',        line(12, 18, 88, 60, 'black')),
    ('dashed',       line(12, 18, 88, 60, 'blue', pattern=DashPattern.DASHED)),
    ('dotted',       line(12, 18, 88, 60, 'green', pattern=DashPattern.DOTTED)),
    ('arrow ->',     line(12, 40, 88, 40, 'red', arrow=True)),
    ('horizontal',   line(12, 40, 88, 40, 'teal')),
    ('vertical',     line(50, 8, 50, 70, 'orange')),
    ('diagonal up',  line(12, 70, 88, 10, 'crimson', arrow=True)),
    ('thick (6px)',  line(12, 18, 88, 60, 'purple', width=6)),
]
for i, (text, ln) in enumerate(cells):
    win.add_child(cell(i, text, ln))

RenderHtml.to_file(root=win, path='line.html')
