from f_gui.pyqt.app import App
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox


class AppQA(App):

    def __init__(self) -> None:
        App.__init__(self, name='Myq')

    def _add_question(self) -> None:
        pass

    def _add_answer(self) -> None:
        pass
