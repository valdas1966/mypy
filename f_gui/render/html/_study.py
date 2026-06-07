
from f_gui.elements import Window, Container, Label, Line
from f_gui.style import Stroke, LineStyle, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds, Point
from f_color import RGB


def create_con_left() -> Container:
    # Yellow panel with a uniform 2px solid black border.
    bounds = Bounds(10, 10, 90, 40)
    border = Border.Factory.all(stroke=Stroke(color=RGB('BLACK'), width=2))
    return Container(bounds=bounds, background=RGB('YELLOW'), border=border)

def create_con_right() -> Container:
    # Yellow panel with a dashed blue border on top + bottom only.
    bounds = Bounds(10, 60, 90, 90)
    edge = Stroke(color=RGB('BLUE'), width=3, style=LineStyle.DASHED)
    border = Border(top=edge, bottom=edge)
    return Container(bounds=bounds, background=RGB('YELLOW'), border=border)

def create_arrow() -> Line:
    # Solid arrow bridging the two containers (left -> right).
    return Line(p1=Point(x=40, y=50), p2=Point(x=60, y=50),
                stroke=Stroke(color=RGB('RED'), width=3), arrow=True)

def create_diagonal() -> Line:
    # Dashed blue diagonal across the whole window.
    return Line(p1=Point(x=0, y=0), p2=Point(x=100, y=100),
                stroke=Stroke(color=RGB('BLUE'), width=2,
                              style=LineStyle.DASHED))

win = Window(background=RGB('WHITE'))
con_left = create_con_left()
con_right = create_con_right()
win.add_child(con_left)
win.add_child(con_right)
win.add_child(create_diagonal())
win.add_child(create_arrow())

RenderHtml.to_file(root=win, path='study.html')

