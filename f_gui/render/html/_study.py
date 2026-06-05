
from f_gui.elements import Window, Container, Label
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds
from f_color import RGB


def create_con_left() -> Container:
    bounds = Bounds(10, 10, 90, 40)
    return Container(bounds=bounds, background=RGB('YELLOW'))

def create_con_right() -> Container:
    bounds = Bounds(10, 60, 90, 90)
    return Container(bounds=bounds, background=RGB('YELLOW'))

win = Window(background=RGB('WHITE'))
con_left = create_con_left()
con_right = create_con_right()
win.add_child(con_left)
win.add_child(con_right)

RenderHtml.to_file(root=win, path='study.html')

