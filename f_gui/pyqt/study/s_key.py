from f_gui.pyqt.app import App
from f_gui.pyqt.window import Window
from f_gui.pyqt.widgets.text_box import TextBox


def on_enter() -> None:
    print('Enter key was pressed!')


def get_text_box() -> TextBox:
    text = TextBox()
    text.set_on_enter(callback=on_enter)
    return text


app = App()

win = Window()
text = get_text_box()
win.add(child=text.widget, rel_x=10, rel_y=30, rel_width=80, rel_height=30)

app.run(win)
