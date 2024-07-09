from f_gui.pyqt.app import App
from f_gui.pyqt.window import Window
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox


def on_enter() -> None:
    print('Enter key was pressed!')


app = App()

win = Window(name='Window')
win.background = 'black'

question = Label()
question.background = 'white'
question.text = 'Hello'
question.font.family = 'heebo'
question.font.is_bold = True
question.font.size = 48
win.add(child=question.widget, rel_x=10, rel_y=30, rel_width=80, rel_height=15)

answer = TextBox()
answer.background = 'white'
answer.font.family = 'heebo'
answer.font.is_bold = True
answer.font.size = 48
answer.set_on_enter(callback=on_enter)
win.add(child=answer.widget, rel_x=10, rel_y=50, rel_width=80, rel_height=15)

app.run(win)
