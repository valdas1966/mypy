from f_gui.pyqt.app import App
from f_gui.pyqt.window import Window
from f_gui.pyqt.container import Container
from f_gui.pyqt.widgets.label import Label


app = App()
win = Window(name='Window')
win._container.background = 'darkgray'
con = Container(name='Container')
con.background = 'black'
# win.add(child=con.widget, rel_x=10, rel_y=10, rel_width=80, rel_height=80)
label = Label()
label.background = 'white'
label.text = 'Hello'
label.font.family = 'heebo'
label.font.is_bold = True
label.font.size = 48
win.add(child=label.widget, rel_x=10, rel_y=30, rel_width=80, rel_height=15)
app.run(win)
