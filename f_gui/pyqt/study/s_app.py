from f_gui.pyqt.app import App
from f_gui.pyqt.container import Container
from f_gui.pyqt.widgets.label import Label


def get_container(name: str, color: str) -> Container:
    con = Container(name=name)
    con.background = color
    return con


def get_red_container() -> Container:
    con = get_container(name='Red', color='Red')
    con.position.relative = (0.5, 0.5, 0.5, 0.5)
    label = Label()
    label.text = 'Label'
    label.position.relative = (0.25, 0.25, 0.5, 0.5)
    con.add(child=label)
    return con


app = App(name='Test')
con_blue = get_container('Blue', 'Blue')
con_blue.position.relative = (0, 0, 0.5, 0.5)
app.add(con_blue)
con_red = get_red_container()
app.add(con_red)
app.run()


