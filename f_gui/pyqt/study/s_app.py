from f_gui.pyqt.app import App
from f_gui.pyqt.window import Window
from f_gui.pyqt.container import Container


app = App()
win = Window(name='Hello World!')
con = Container()
con.background = 'black'
win.add(w=con.widget, x=50, y=50, width=1820, height=880)
app.run(win)
