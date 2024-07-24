from f_gui.pyqt.app import App
from f_gui.pyqt.container import Container


def get_container(name: str, color: str) -> Container:
    con = Container(name=name)
    con.background = color
    return con


app = App(name='Test')
con_blue = get_container('Blue', 'Blue')
con_blue.position.relative = (0, 0, 0.5, 0.5)
app.add(con_blue)
con_red = get_container(name='Red', color='Red')
con_red.position.relative = (0.5, 0.5, 0.5, 0.5)
app.add(con_red)
app.run()


