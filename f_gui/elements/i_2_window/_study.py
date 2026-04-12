from f_gui.elements import Window, Container, Label
from f_ds.geometry import Bounds


def add_container_left(win: Window) -> None:
    bounds_con = Bounds(top=20, left=10, bottom=80, right=45)
    con = Container(name='Container Left', bounds=bounds_con)
    bounds_label = Bounds(top=20, left=20, bottom=40, right=80)
    label = Label(name='Label Left', text='Left', bounds=bounds_label)
    con.add_child(child=label)
    win.add_child(child=con)


def add_container_right(win: Window) -> None:
    bounds_con = Bounds(top=20, left=55, bottom=80, right=90)
    con = Container(name='Container Right', bounds=bounds_con)
    bounds_label = Bounds(top=20, left=20, bottom=40, right=80)
    label = Label(name='Label Right', text='Right', bounds=bounds_label)
    con.add_child(child=label)
    win.add_child(child=con)


win = Window(name='Window')
add_container_left(win)
add_container_right(win)
win.to_html(path='_study.html')
