from f_gui.pyqt.app import App
from f_gui.pyqt.window import Window
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox
from PyQt5.QtWidgets import QWidget


def on_enter() -> None:
    print('Enter key was pressed!')


def create_question() -> Label:
    question = Label('Question')
    question.background = 'white'
    question.text = 'Hello'
    question.font.family = 'heebo'
    question.font.is_bold = True
    question.font.size = 48
    return question


def create_answer() -> TextBox:
    answer = TextBox('Answer')
    answer.background = 'white'
    answer.font.family = 'heebo'
    answer.font.is_bold = True
    answer.font.size = 48
    answer.set_on_enter(callback=on_enter)
    return answer


app = App('Myq')
app.background = 'black'
app.add(child=create_question(),
        rel_x=10, rel_y=30, rel_width=80, rel_height=15)
app.add(child=create_answer(),
        rel_x=10, rel_y=50, rel_width=80, rel_height=15)
app.run()
